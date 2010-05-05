<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php

$exe_print="\"c:\\Program Files\\Ghostgum\\gsview\\gsprint.exe\"   ";
$exe_python="c:\\Python24\\python.exe ..\\print\\demon.pyw";

//$dir_imprime=""\Oyak\work\*";
$dir_imprime="\impprint\*";
//$dir_imprime="test\*";

$header="";
$orientation="portrait";
$nb_lignes_imprime=18;

include("../inc/header.php");
$debug=0;
$not_deleting=0;

// lecture des masques
$dir=".";

$preambule_portrait=join("",file("$dir/preambule.tex"));
$preambule_landscape=join("",file("$dir/preambule_landscape.tex"));
$header=join("",file("$dir/header.tex"));
$footer=join("",file("$dir/footer.tex"));
$conclusion=join("",file("$dir/conclusion.tex"));
$printer="default";
$copies=1;


$nb_pages_portrait=0;
$nb_pages_landscape=0;
$filenames=glob($dir_imprime);

if ($filenames) {


	foreach ($filenames as $filename) {

		$orientation="PORTRAIT";
		// traitement fichier en cours
		echo "<BR> Traitement impression $filename................................................";
		$out=make_imprime($filename);

		// ecriture vers le fichier all_portrait ou all_landscape.tex


		if (strstr($orientation,"PAYSAGE")) {
			if ($nb_pages_landscape>0) {
				fwrite($file_landscape_out,"\\clearpage");
			}
			else {
				@unlink("all_landscape.tex");
				@unlink("all_landscape.dvi");
				@unlink("all_landscape.ps");
				@unlink("all_landscape.aux");
				@unlink('c:/Oyak/imprime_landscape.ps');
				$file_landscape_out=fopen("all_landscape.tex","w");
				fwrite($file_landscape_out,$preambule_landscape);
			}
			$nb_pages_landscape=$nb_pages_landscape+1;
			fwrite($file_landscape_out,$out);
		}
		else {
			if ($nb_pages_portrait>0) {
				fwrite($file_portrait_out,"\\clearpage");
			}
			else {
				@unlink("all_portrait.tex");
				@unlink("all_portrait.dvi");
				@unlink("all_portrait.ps");
				@unlink("all_portrait.aux");
				@unlink('c:/Oyak/imprime_portrait.ps');
				$file_portrait_out=fopen("all_portrait.tex","w");
				fwrite($file_portrait_out,$preambule_portrait);
			}
			$nb_pages_portrait=$nb_pages_portrait+1;
			fwrite($file_portrait_out,$out);
		}

		if ($not_deleting) {
			echo "<BR> Effacement $filename NON FAIT   NON FAIT.... <BR> <BR>.";
		}
		else {
			unlink($filename);
			echo "<BR> Effacement $filename OK.... <BR> <BR>.";
		}
	}

	if ($nb_pages_portrait) {
		fwrite($file_portrait_out,$conclusion);
		fclose($file_portrait_out);

		system("compile_portrait.bat > out",$status);
		//print "res=$status";
		$lines=file("out");
		$l=array_shift($lines);
		$msg="";
		while($l){
			$msg=$msg."$l <BR>";
			$l=array_shift($lines);
		}

		if (ereg("Emergency stop",$msg) or ereg("No pages of output",$msg))  {
			$msg=ereg_replace("^.*aux))","ERREUR : ",$msg);
			$msg=ereg_replace("No pages of output.*$","No pages of ouput",$msg);
			print "<BR> <BOLD> <br> <B> ERREUR D'INTERPRETATION dans $filename !!!! </B> <BR> $msg <BR>";
		}
		else {
			print_all("portrait");
			print "<BR> <BOLD> <br> <B> semble ok dans $filename !!!! </B> <BR> $msg <BR>";
		}

	}

	if ($nb_pages_landscape) {
		fwrite($file_landscape_out,$conclusion);
		fclose($file_landscape_out);

		system("compile_landscape.bat > out");
		//print "res=$status";

		print_all("landscape");

	}

	print "<BR> ".($nb_pages_portrait+$nb_pages_landscape)." crées<BR> ";


}
else {
	print "pas de imprime en attente <BR>";
}


print "<BR> <a href='../admin/index.php'>  Retour Administration </a>\n";


function print_all($orientation) {
	global $printer;

	@mkdir ("c:/Oyak/ToPrint",0755);
	if ($printer=="default") {
		copy ("all_$orientation.ps", "c:/Oyak/ToPrint/imprime_$orientation.ps");
		copy ("all_$orientation.ps", "c:/Oyak/imprime_$orientation.ps");
	}
	else {
		@mkdir ("c:/Oyak/ToPrint/$printer",0755);
		copy ("all_$orientation.ps", "c:/Oyak/ToPrint/$printer/imprime_$orientation.ps");
		copy ("all_$orientation.ps", "c:/Oyak/imprime_$orientation.ps");
	}
}

function make_imprime ($file) {
	global $debug, $orientation,$header, $footer,$body,$body_vide,
	$nb_lignes_imprime,$footer2,$header2,$printer,$copies;


	$document="";
	$nb_ligne=0;
	$total=0;
	$out=$header;

	$hline='\hline'."\n";

	$lines=file($file);

	$nb_ligne=0;

	foreach ($lines as $line) {
		$champs = split("!",$line);
		$what=array_shift($champs);

		print "<BR> what  = $what";
		if (ereg("^Z0,1",$what))  {
			// nom de l'imprimante, nombre d'impression, type de document
			$printer=array_shift($champs);
			$copies=array_shift($champs);
			$document=array_shift($champs);
			$orientation=array_shift($champs);
			print " <-- <B> OK </B>";
			next;
		}

		if (ereg("^EJECT",$what))  {
			// saut de page
			$out=$out.$footer."\n"."\\clearpage".$header."\n";
			print " <-- <B> OK </B>";
			next;
			$box_open=0;
		}

		{


			$x=array_shift($champs);
			$y=array_shift($champs);
	
			if (!($x=="." and $y==".")) {  
				if ($box_open) {
					$out=$out."}}\n";	
				}
				$out=$out.'\put('.$x.','.(29-$y).'){\shortstack[l]{' ;
				$box_open=1;
				
			}
			else {
				$out=$out.'\\\\'."\n";
			}

			// texte simple
			if ($what=="TXT") {
				$texte=array_shift($champs);
				$texte=ereg_replace('&','\&',$texte);
				$texte=ereg_replace('{','\{',$texte);
				$texte=ereg_replace('}','\}',$texte);
				$texte=ereg_replace('%','\%',$texte);
				$out=$out."$texte";
				print " <-- <B> OK </B>";
				next;
			}

			// tableau
			if ($what=="TAB") {
				$tailles=split("=",array_shift($champs));

				$out=$out.'\mbox{\begin{tabular}[t]{';

				$col=1;
				while ($taille=array_shift($tailles)) {
					$format_cell[$col]="p{".$taille."cm}";
					$out=$out.$format_cell[$col];
					$col=$col+1;
				}
				$out=$out."}\n";

				for ($c=0;$c<$col-2;$c++) {
					$out = $out." & ";
				}
				$out=$out.'\\\\';

				$nb_lin=0;
				while ($line=array_shift($champs)) {
					$cells=split("=",$line);
					$nb_int=0;

					$col=1;
					while ($cell=array_shift($cells)) {

						$fields=split(";",$cell);
						$texte=array_shift($fields);
						$texte=ereg_replace('&','\&',$texte);
						$texte=ereg_replace('{','\{',$texte);
						$texte=ereg_replace('}','\}',$texte);
						$texte=ereg_replace('%','\%',$texte);
						$format=array_shift($fields);
						$masque='\multicolumn{1}{'.$format_cell[$col].'}{%s}';

						// y a-t-il un format associe a la scene?
						if ($format) {
							$cadrage=substr($format,0,1);
							$bords  =substr($format,1,1);
							$couleur=substr($format,2,1);
							$font   =substr($format,3,1);
							$nb_cols=substr($format,4,2);
							if (!$nb_cols) {$nb_cols=1;}

							//$out=$out."\n\n %===> texte=$texte; format=$format; cadrage='$cadrage'; bords='$bords'; couleur='$couleur'; font='$font'; nb_cols='$nb_cols';\n";

							$bord_left=""; $bord_right="";
							switch($bords) {
								case "g": $bord_left="|";                  break;
								case "d": $bord_right="|";                 break;
								case "c": $bord_left="|"; $bord_right="|"; break;
								default : $bord_left=""; $bord_right="";
							}

							switch($cadrage) {
								case "d" : $cadrage="r"; break;
								case "g" : $cadrage="l"; break;
								case "." : $cadrage=$format_cell[$col]; break;
							}

							$bord_left=""; $bord_right="";
							switch($bords) {
								case "g": $bord_left="|";                  break;
								case "d": $bord_right="|";                 break;
								case "c": $bord_left="|"; $bord_right="|"; break;
								default : $bord_left=""; $bord_right="";
							}

							switch($font) {
								case "g": $in='\textbf{%s}'; break;
								case "i": $in='\textsl{%s}'; break;
								case "l": $in='\large{%s}'; break;
								case "s": $in='\small{%s}'; break;
								case "f": $in='\footnotesize{%s}'; break;
								default : $in='%s';
							}

							$masque='\multicolumn{'.$nb_cols.'}{'.$bord_left.$cadrage.$bord_right.'}{'.$in.'}';

							switch($cadrage) {
								case "T": $masque=$hline; break;
								case "t": $masque='\cline{'.$col.'-'.($col+$nb_cols-1).'}';  break;
							}

						}

						if ($col>1) { $out = $out.'&';}
						$col=$col+1;
						$out=$out.sprintf($masque,$texte);
					}

					if ($masque!=$hline) {
						$out=$out.'\\\\ '."\n";
					}
				}


				$out=$out.'\end{tabular}}';
				print " <-- <B> OK </B>";
				next;
			}

			

		}
		
	}
//	$out=$out."}}\n";
	$out=$out.$footer."\n\n";


	$out=ereg_replace("__PETIT__","{\\tiny ",$out);
	$out=ereg_replace("__GRAS__","\\textbf{",$out);
	$out=ereg_replace("__GRIS__","\\colorbox[gray]{0.8}{ ",$out);
	$out=ereg_replace("__petit__","}",$out);
	$out=ereg_replace("__gras__","}",$out);
	$out=ereg_replace("__gris__","}",$out);


	return $out;
}





?>

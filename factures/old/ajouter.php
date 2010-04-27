<?php include("../inc/conf.php"); ?>
<?php include("../inc/fonctions.php"); ?>
<?php include("../verif.php"); ?>
<?php

if ($action == "send")
{
   if ($id_clt == "0")
   {
   $msg = "Veuillez choisir un client";
   }
   else
   {
      if ($id_taux == "0")
	  {
	  $msg = "Veuillez choisir un taux";
	  }
	  else
	  {
	     if ($type == "")
		 {
		 $msg = "Veillez choisir le type (Facture ou Devis)";
		 }
		 else
		 {
		    if ($etat == "")
			{
			$msg = "Veuillez sélectionner l'etat";
			}
			else
			{
			$req = mysql_query("insert into ".$prefixe_table."factures values ('','$id_clt','$id_taux','$escompte','$date','$type','$etat')");
			
			$req = mysql_query("select max(num) from ".$prefixe_table."factures");
			$max_num = mysql_result($req,0,"max(num)");
			
			mysql_close($connect_db);
			header("location: modifier.php?id_facture=$max_num");
			exit();
			}
		 }
	  }
   }
}


?>
<?php include("../inc/header.php"); ?>

<?php

if ($msg != "")
{
$msg = str_replace("+"," ",$msg);
echo("<center><font color=\"#ff0000\"><b>$msg</b></font></center><br>");
}

?>

<form action="ajouter.php" method="post">
<input type="hidden" name="action" value="send">

<table border="0" align="center">
   <tr>
      <td><b>Client</b> :</td>
	  <td><select name="id_clt" style="width: 320px">
	  <option value="0">Choisissez</option>
	  <?php
	  
	  $req = mysql_query("select id,nom,prenom from ".$prefixe_table."clients order by nom,prenom");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $nom = $ligne["nom"];
	  $prenom = $ligne["prenom"];
	  
	  echo("<option value=\"$id\"");
	  if ($id == $id_clt){echo(" selected");}
	  echo(">$nom $prenom</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td><b>Taux T.V.A</b> :</td>
	  <td><select name="id_taux" style="width: 320px">
	  <option value="0">Choisissez</option>
	  <?php
	  
	  $req = mysql_query("select * from ".$prefixe_table."taux_tva order by taux");
	  while($ligne = mysql_fetch_array($req))
	  {
	  $id = $ligne["id"];
	  $taux = $ligne["taux"];
	  echo("<option value=\"$id\"");
	  if ($id == $id_taux){echo(" selected");}
	  echo(">$taux</option>");
	  }
	  
	  ?>
	  </select></td>
   </tr>
   <tr>
      <td><b>Escompte</b> :</td>
	  <td><input type="text" name="escompte" size="15" value="<?php echo("$escompte"); ?>"> %</td>
   </tr>
   <tr>
      <td><b>Date</b> :</td>
	  <td><input type="text" name="date" size="30" value="<?php echo("$date"); ?>"> (AAAA-MM-JJ)</td>
   </tr>
   <tr>
      <td><b>Type</b> :</td>
	  <td><input type="radio" name="type" value="d" <?php if($type == "d"){echo("checked");} ?>> Devis 
	  <input type="radio" name="type" value="f" <?php if($type == "f"){echo("checked");} ?>> Facture</td>
   </tr>
   <tr>
      <td><b>Etat</b> :</td>
	  <td><input type="radio" name="etat" value="0" <?php if($etat == "0"){echo("checked");} ?>> En cours
	  <input type="radio" name="etat" value="1" <?php if($etat == "1"){echo("checked");} ?>> Terminé
	  <input type="radio" name="etat" value="2" <?php if($etat == "2"){echo("checked");} ?>> Terminé / payé  
	  <input type="radio" name="etat" value="3" <?php if($etat == "3"){echo("checked");} ?>> Annulé</td>
   </tr>
</table>

<br>

<center><input type="submit" value="Ajouter"></center>

</form>

<center>
<a href="index.php">Retour</a>
</center>

<?php include("../inc/footer.php"); ?>
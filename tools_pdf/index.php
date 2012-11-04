<?php


require('fpdf17/fpdf.php');

// mode paysage, a4, etc.

$pdf=new FPDF('L','mm','A4');
$pdf->Open();

// champs facultatifs

$pdf->SetAuthor('Hyperion - Ben Hermans');
$pdf->SetCreator('CygnusEd 4.21 & Fpdf');
$pdf->SetTitle('Amiwest AmigaOS 4 Presentation');
$pdf->SetSubject('Remix by bIgdAn');

// on charge les 83 gfx...

$pdf->SetMargins(0,0);
for ($i=1; $i<4; $i++) {
$pdf->AddPage();
//$pdf->Image('Diapositive'.$i.'.JPG',0,0,297,210,'JPEG');
$pdf->Image('../print/factures/persepolis.jpg',0,0,297,210,'JPEG');
}

// Et on affiche le pdf généré... (ou on le sauvegarde en local)
$pdf->Output('facture.pdf','D');

?>



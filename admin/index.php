<?php 
include("../inc/conf.php"); 
include("../inc/fonctions.php"); 
print "</HEAD>";
include("../inc/header.php"); 

	$compteur=0;
	$query="select compteur from  ".$prefixe_table."compteur ";
	$req = mysql_query($query);
	while($ligne = mysql_fetch_array($req))
	{ $compteur0 = $ligne["compteur"];
	   if ($compteur0>$compteur) {$compteur=$compteur0;}
	}
		

if (!$message) { $message="&nbsp;";}
	
?>
  <center>
  <table> <tr> 
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> modifier la base </b> </td> </tr> <tr>
    <td rowspan=3>    
        <a href="./perform_sql.php?order=base_init">Initialiser la base</a><br>
       	<a href="./perform_sql.php?order=base_exemple">Créer une base d'exemple</a><br>
    	<a href="../produits/check.php">Afficher les anomalies </a><br>
	<a target=mysqladmin href="../../phpmyadmin/index.php">Console SQL</a></td>
   <td align=right>
   <form  enctype="multipart/form-data"  action="update_table.php3" method="post">
  			  fichier clients  : &nbsp;
        <input type="file" name="file_client[]"  /> </td> </tr> <tr> <tr> <td align=right>
  			  fichier produit  : &nbsp;
        <input type="file" name="file_produit[]"  /> </td> <td>
  			<input type="submit" name="SQL" value="Mettre a jour" /> 
    </td> </form>
   </tr>
    <tr></tr> 
    <tr></tr> 
    <tr></tr> 
    <tr></tr> 
    <tr></tr> 
    <tr></tr> 
    <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> voir la base depuis la device </b> </td> </tr> <tr>
    <td /> <a href="../query/get_data.php?clients=1&header=1">Liste Brute Client</a></td> 
    <td /> <a href="../query/get_data2.php?clients=1&header=1">Liste Brute Client/Time</a></td> 
    <td /> <a href="../query/get_data.php?clients=1&header=1&date=1">Date Brute Client</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?fournisseurs=1&header=1">Liste Brute Fournisseur</a></td>
    <td /> <a href="../query/get_data2.php?fournisseurs=1&header=1">Liste Brute Fournisseur/Time</a></td>
    <td /> <a href="../query/get_data.php?fournisseurs=1&header=1&date=1">Date Brute Fournisseur</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?produits=1&header=1">Liste Brute Produit</a></td>
    <td /> <a href="../query/get_data2.php?produits=1&header=1">Liste Brute Produit/Time</a></td>
    <td /> <a href="../query/get_data.php?produits=1&header=1&date=1">Date Brute Produit</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?vendeurs=1&header=1">Liste Brute Vendeur</a></td>
    <td /> <a href="../query/get_data2.php?vendeurs=1&header=1">Liste Brute Vendeur/Time</a></td>
    <td /> <a href="../query/get_data.php?vendeurs=1&header=1&date=1">Date Brute Vendeur</a></td>
</tr>
<tr >
    <td /> <a href="../query/get_data.php?releases=1&header=1">Liste Brute releases</a></td>
    <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> gérer les commandes</b> </td> </tr> <tr>
    <tr >
    <td rowspan=4> le compteur commandes <br> est a <?php echo $compteur ?> </td> 
    <td> <a href="reinit_compteur.php"> Mettre a zero </a></td>
</tr>
<tr >
      <td> <a href="../query/unit_test.php">Créer des commandes de tests</a></td>
</tr><tr>
      <td> <a href="../query/index.php?header=1">Tester envoi de commande a la base</a></td>
       </tr>
<tr >
      <td > <a href="../query/interroge.php?header=1">Tester envoi de requete d'interrogation a la base</a></td>
  </tr>
<?php 
include("git_command.php"); 
?>
</table>
</center>


<script type="text/javascript">
<!--
    var dbBoxSetupDone = false;
    function dbBoxSetup() {
        if (dbBoxSetupDone != true) {
            if (parent.frames.queryframe && parent.frames.queryframe.document.left && parent.frames.queryframe.document.left.lightm_db) {
                parent.frames.queryframe.document.left.lightm_db.value = 'oyak';
                dbBoxSetupDone = true;
            } else {
                setTimeout("dbBoxSetup();",500);
            }
        }
    }
    if (parent.frames.queryframe && parent.frames.queryframe.document && parent.frames.queryframe.document.queryframeform) {
        parent.frames.queryframe.document.queryframeform.db.value = "oyak";
        parent.frames.queryframe.document.queryframeform.table.value = "";
    }
    if (parent.frames.queryframe && parent.frames.queryframe.document && parent.frames.queryframe.document.left && parent.frames.queryframe.document.left.lightm_db) {
        selidx = parent.frames.queryframe.document.left.lightm_db.selectedIndex;
        if (parent.frames.queryframe.document.left.lightm_db.options[selidx].value == "oyak") {
            parent.frames.queryframe.document.left.lightm_db.options[selidx].text = "oyak (10)";
        } else {
            parent.frames.queryframe.location.reload();
            setTimeout("dbBoxSetup();",2000);
        }
    }
    
    function reload_querywindow () {
        if (parent.frames.queryframe && parent.frames.queryframe.querywindow && !parent.frames.queryframe.querywindow.closed && parent.frames.queryframe.querywindow.location) {
                        if (!parent.frames.queryframe.querywindow.document.sqlform.LockFromUpdate || !parent.frames.queryframe.querywindow.document.sqlform.LockFromUpdate.checked) {
                parent.frames.queryframe.querywindow.document.querywindow.db.value = "oyak";
                parent.frames.queryframe.querywindow.document.querywindow.query_history_latest_db.value = "oyak";
                parent.frames.queryframe.querywindow.document.querywindow.table.value = "";
                parent.frames.queryframe.querywindow.document.querywindow.query_history_latest_table.value = "";

                // no sql query update

                parent.frames.queryframe.querywindow.document.querywindow.submit();
            }
                    }
    }

    function focus_querywindow(sql_query) {
        if (parent.frames.queryframe && parent.frames.queryframe.querywindow && !parent.frames.queryframe.querywindow.closed && parent.frames.queryframe.querywindow.location) {
            if (parent.frames.queryframe.querywindow.document.querywindow.querydisplay_tab != 'sql') {
                parent.frames.queryframe.querywindow.document.querywindow.querydisplay_tab.value = "sql";
                parent.frames.queryframe.querywindow.document.querywindow.query_history_latest.value = sql_query;
                parent.frames.queryframe.querywindow.document.querywindow.submit();
                parent.frames.queryframe.querywindow.focus();
            } else {
                parent.frames.queryframe.querywindow.focus();
            }

            return false;
        } else if (parent.frames.queryframe) {
            new_win_url = 'querywindow.php?sql_query=' + sql_query + '&lang=fr-utf-8&server=1&collation_connection=utf8_general_ci&db=oyak';
            parent.frames.queryframe.querywindow=window.open(new_win_url, '','toolbar=0,location=0,directories=0,status=1,menubar=0,scrollbars=yes,resizable=yes,width=550,height=310');

            if (!parent.frames.queryframe.querywindow.opener) {
               parent.frames.queryframe.querywindow.opener = parent.frames.queryframe;
            }

            // reload_querywindow();
            return false;
        }
    }

    reload_querywindow();

//-->
</script>


</body>

</html>


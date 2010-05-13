<?php
?>
    <tr>
    <td bgcolor="#99CCCC" colspan=6 align=center>  <b> gerer les versions</b> </td> </tr> <tr>
    <tr >
    	<td> <a href="git.php?action=log"> historique </a></td>
    	<td> <a href="git.php?action=branch -a"> version </a></td>
	<td> <a href="git.php?action=diff"> diff </a></td>
    </tr> <tr>
    	<td> <a href="git.php?action=push"> synchronise </a></td>
    <td align=right>
   <form  enctype="multipart/form-data"  action="git.php" method="post">
  			  Sauvegarde  : &nbsp;
        <input type=text name=comment value="commentaire"  /> 
	<input type=hidden name=action value="commit -a  "  /> 
  			<input type="submit"  value="Go" /> 
    </td> </form>
    </tr>
<?php
?>
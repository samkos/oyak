
<!-- TWO STEPS TO INSTALL CHECKBOX CHANGER:

  1.  Copy the coding into the HEAD of your HTML document
  2.  Add the last code into the BODY of your HTML document  -->

<!-- STEP ONE: Paste this code into the HEAD of your HTML document  -->

<HEAD>

<SCRIPT LANGUAGE="JavaScript">

<!-- This script and many more are available free online at -->
<!-- The JavaScript Source!! http://javascript.internet.com -->

<!-- Begin
function checkAll() {
for (var j = 1; j <= 14; j++) {
box = eval("document.checkboxform.C" + j); 
if (box.checked == false) box.checked = true;
   }
}

function uncheckAll() {
for (var j = 1; j <= 14; j++) {
box = eval("document.checkboxform.C" + j); 
if (box.checked == true) box.checked = false;
   }
}

function switchAll() {
for (var j = 1; j <= 14; j++) {
box = eval("document.checkboxform.C" + j); 
box.checked = !box.checked;
   }
}
//  End -->
</script>
</HEAD>

<!-- STEP TWO: Copy this code into the BODY of your HTML document  -->

<BODY>

<center>
<form name=checkboxform>
<input type=checkbox name=C1 checked>C1<br>
<input type=checkbox name=C2 checked>C2<br>
<input type=checkbox name=C3 checked>C3<br>
<input type=checkbox name=C4 checked>C4<br>
<input type=checkbox name=C5 checked>C5<br>
<input type=checkbox name=C6 checked>C6<br>
<input type=checkbox name=C7 checked>C7<br>
<input type=checkbox name=C8 checked>C8<br>
<input type=checkbox name=C9 checked>C9<br>
<input type=checkbox name=C10 checked>C10<br>
<input type=checkbox name=C11 checked>C11<br>
<input type=checkbox name=C12 checked>C12<br>
<input type=checkbox name=C13 checked>C13<br>
<input type=checkbox name=C14 checked>C14<br>
<br>
<input type=button value="Check All" onClick="checkAll()"><br>
<input type=button value="Uncheck All" onClick="uncheckAll()"><br>
<input type=button value="Switch All" onClick="switchAll()"><br>
</form>
</center>

<p><center>
<font face="arial, helvetica" size="-2">Free JavaScripts provided<br>
by <a href="http://javascriptsource.com">The JavaScript Source</a></font>
</center><p>

<!-- Script Size:  1.94 KB -->
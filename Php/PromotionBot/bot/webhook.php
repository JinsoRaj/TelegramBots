<?php
include_once('config/config.php');
include_once('tg.class.php');
$body = file_get_contents('php://input');
$arr = json_decode($body, true); 
$tg = new tg(TGKEY);
$db_host = DB_HOST;
$db_user = DB_USER;
$db_password = DB_PASSWORD;
$db_name = DB_NAME;
$tg_id = $arr['message']['chat']['id'];
$rez_kb = array();
$message_text = $arr['message']['text'];
$tg->sendChatAction($tg_id);
$sms_rev='';
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_name);
$query = "SELECT f_name, l_name FROM customers WHERE f_name='$message_text'";
$result = $mysqli->query($query);
$row = $result->fetch_assoc();
  switch($message_text){
   case '/start':
		$sms_rev = 'Hello. Welcome to Miigom Bot. Come on.';
   break;
   //case define("mixedCASE", $row["f_name"], TRUE);
      case $row["f_name"]:
		$sms_rev = $row["l_name"];
   break;
      default:
		$sms_rev ='The command is not correct. Maybe you spelled the word (s) correctly.';
   break; 
}   
$tg->send($tg_id, $sms_rev, $rez_kb);
exit('ok');
?>
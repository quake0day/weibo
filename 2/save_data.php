<?php
session_start();
$u_id = $_GET["uid"];

include_once( 'config.php' );
include_once( 'saet2.ex.class.php' );
$mysql = new SaeMysql();
$sql = "select token from `token` where id = 1";
$data = $mysql->getData($sql);
$token_new = $data[0]['token'];
//从POST过来的signed_request中提取oauth2信息
$c = new SaeTClient( WB_AKEY , WB_SKEY ,$token_new ,'' );


//$u_id = "1651712685";
$msg  = $c->show_user($u_id); // done
if($msg === false || $msg === null){
	echo "Error occured";
	return false;
}
if(isset($msg['error_code']) && isset($msg['error'])){
	echo (' Error_code:' . $msg['error_code'] .'; Error:' .$msg['error']);
	return false;
}
echo($msg['id'].':'.$msg['name'].' '.$msg['followers_count'].' '.$msg['friends_count']);


$sql = "INSERT INTO `app_analysisme`.`data` (`id`, `uid`, `followers`, `friends`, `time`) VALUES (NULL, '".$msg['id']."', '".$msg['followers_count']."', '".$msg['friends_count']."', ".time().")";
$mysql->runSql($sql);
if( $mysql->errno() != 0)
{
	die("Error:".$mysql->errmsg());
}
$mysql->closeDb();	

?>



</body>
</html>

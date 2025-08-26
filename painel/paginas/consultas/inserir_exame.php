<?php 
require_once("../../../conexao.php");

$id_pac = $_POST['id_paciente'];
$exame = @$_POST['exame'];
$exame2 = @$_POST['exame2'];

$clinica = 'Sim';
if($exame == ""){
	$exame = $exame2;
	$clinica = 'Não';
}

@session_start();
$id_usuario = $_SESSION['id'];

$query = $pdo->prepare("INSERT INTO exames SET paciente = '$id_pac', medico = '$id_usuario', exame = :exame, clinica = :clinica, data = curDate()");

$query->bindValue(":exame", "$exame");
$query->bindValue(":clinica", "$clinica");
$query->execute();

echo 'Inserindo com Sucesso';

?>
<?php 
require_once("../../../conexao.php");

$id_pac = $_POST['id_paciente'];
$remedio = $_POST['remedio'];
$quantidade = $_POST['quantidade'];
$uso = $_POST['uso'];

@session_start();
$id_usuario = $_SESSION['id'];

$query = $pdo->prepare("INSERT INTO receita SET paciente = '$id_pac', medico = '$id_usuario', remedio = :remedio, quantidade = :quantidade, uso = :uso, data = curDate()");

$query->bindValue(":remedio", "$remedio");
$query->bindValue(":quantidade", "$quantidade");
$query->bindValue(":uso", "$uso");
$query->execute();

echo 'Inserindo com Sucesso';

?>
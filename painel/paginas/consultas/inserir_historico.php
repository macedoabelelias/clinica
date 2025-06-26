<?php 
$tabela = 'historico_paciente';
require_once("../../../conexao.php");

$historico = $_POST['historico'];
$id_pac = $_POST['id_pac'];
$id_con = $_POST['id_con'];

@session_start();
$id_usuario = $_SESSION['id'];
$nome_usuario = $_SESSION['nome'];

$query = $pdo->prepare("INSERT INTO $tabela SET paciente = '$id_pac', descricao = :historico, data = curDate(), consulta = '$id_con', funcionario = '$id_usuario', nome_funcionario = '$nome_usuario'");
	
$query->bindValue(":historico", "$historico");

$query->execute();

echo 'Salvo com Sucesso';
 ?>
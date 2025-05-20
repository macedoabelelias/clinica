<?php 
$tabela = 'historico_paciente';
require_once("../../../conexao.php");

$id = $_POST['id'];

$pdo->query("DELETE FROM $tabela where id = '$id'");
echo 'Excluído com Sucesso';


?>
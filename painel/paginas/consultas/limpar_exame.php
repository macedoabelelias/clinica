<?php 
$tabela = 'exames';
require_once("../../../conexao.php");

$id = $_POST['id_paciente'];

$pdo->query("DELETE FROM $tabela where paciente = '$id'");
echo 'Excluído com Sucesso';


?>
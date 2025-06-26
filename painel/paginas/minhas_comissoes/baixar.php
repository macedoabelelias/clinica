<?php 
require_once("../../../conexao.php");
$tabela = 'pagar';

$id = $_POST['id'];

$pdo->query("UPDATE $tabela SET pago = 'Sim' where id = '$id'");
echo 'Baixado com Sucesso';
 ?>
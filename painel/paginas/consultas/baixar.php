<?php 
require_once("../../../conexao.php");
$tabela = 'agendamentos';

$id = $_POST['id'];

$pdo->query("UPDATE $tabela SET status = 'Finalizado' where id = '$id'");
echo 'Baixado com Sucesso';
 ?>
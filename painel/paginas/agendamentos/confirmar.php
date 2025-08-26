<?php 
$tabela = 'agendamentos';
require_once("../../../conexao.php");

$id = $_POST['id'];

$query = $pdo->query("SELECT * FROM $tabela where id = '$id'");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$cliente = $res[0]['paciente'];
$usuario = $res[0]['funcionario'].'';
$data = $res[0]['data'];
$hora = $res[0]['hora'];
$hash = $res[0]['hash'];

$dataF = implode('/', array_reverse(explode('-', $data)));
$horaF = date("H:i", strtotime($hora));

$query = $pdo->query("SELECT * FROM pacientes where id = '$cliente'");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$nome_cliente = $res[0]['nome'];
$telefone = $res[0]['telefone'];

$pdo->query("UPDATE $tabela SET status = 'Confirmado' where id = '$id'");

echo 'Confirmado com Sucesso';

if($token != ""){
	
		$telefone_envio = '55'.preg_replace('/[ ()-]+/' , '' , $telefone);

		$mensagem = '*'.$nome_sistema.'* %0A';
		$mensagem .= '_Agendamento Confirmado_ %0A';
		$mensagem .= '*Data:* '.$dataF.' %0A';	
		$mensagem .= '*Hora:* '.$horaF.' %0A%0A';			
		require("../../apis/texto.php");
	
}	

if($hash != ""){
	require("../../apis/excluir.php");
}

?>
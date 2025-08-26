<?php 
$tabela = 'receber';
require_once("../conexao.php");

$dataInicial = $_POST['dataInicial'];
$dataFinal = $_POST['dataFinal'];
$convenio = $_POST['convenio'];
$pgto = $_POST['pgto'];
$valor = $_POST['valor'];
$obs = $_POST['obs'];

@session_start();
$id_usuario = @$_SESSION['id'];

$query2 = $pdo->query("SELECT * from convenios where id = '$convenio'");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
$linhas2 = @count($res2);
$nome_convenio = $res2[0]['nome'];

$pdo->query("UPDATE agendamentos SET pago = 'Sim' where data >= '$dataInicial' and data <= '$dataFinal' and convenio = '$convenio' and pago = 'Não'");

$query = $pdo->prepare("INSERT INTO $tabela SET descricao = '$nome_convenio', cliente = '0', valor = '$valor', data_venc = curDate(), data_pgto = curDate(), frequencia = '0', saida = '$pgto', data_lanc = curDate(), usuario_lanc = '$id_usuario', usuario_pgto = '$id_usuario', arquivo = 'sem-foto.png', pago = 'Sim', referencia = 'Procedimento', obs = :obs, convenio = '$convenio'");

$query->bindValue(":obs", "$obs");

$query->execute();

echo 'Salvo com Sucesso';
 ?>
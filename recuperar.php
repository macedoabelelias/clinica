<?php 
require_once("conexao.php");
$email = $_POST['email'];

$query = $pdo->prepare("SELECT * from usuarios where email = :email");
$query->bindValue(":email", "$email");
$query->execute();
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$linhas = @count($res);
if($linhas > 0){
	$senha = $res[0]['senha'];
	//ENVIAR O EMAIL COM A SENHA
	$destinatario = $email;
	$assunto = $nome_sistema . ' - Recuperação de Senha';
	$mensagem = 'Sua senha é ' .$senha;
	$cabecalhos = "From: ".$email_sistema;

	@mail($destinatario, $assunto, $mensagem, $cabecalhos);
	echo 'Recuperado';
}else{
echo 'Email não Cadastrado!';
}	
 ?>

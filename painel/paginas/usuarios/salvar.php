<?php
$tabela = 'usuarios';
require_once("../../../conexao.php");

$nome = $_POST['nome'];
$email = $_POST['email'];
$telefone = $_POST['telefone'];
$nivel = $_POST['nivel'];
$endereco = $_POST['endereco'];
$senha = '123';
$senha_crip = md5($senha);

$query = $pdo->prepare("INSERT INTO usuarios SET nome = :nome, email = :email, 
    senha = '$senha', senha_crip = '$senha_crip', nivel = '$nivel', ativo = 'Sim', 
    foto = 'sem-foto.jpg', telefone = :telefone, data = curDate(), endereco = :endereco");
 $query->bindValue(":nome", "$nome");
 $query->bindValue(":email", "$email");
 $query->bindValue(":telefone", "$telefone");
 $query->bindValue(":endereco", "$endereco");
 $query->execute();

 echo 'Salvo com Sucesso';
?>
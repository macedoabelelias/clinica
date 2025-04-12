<?php
$tabela = 'convenios';
require_once("../../../conexao.php");

$nome = $_POST['nome'];
$comissao = $_POST['comissao'];
$id = $_POST['id'];


//validação nome
$query = $pdo->query("SELECT * from $tabela where nome = '$nome'");    
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$id_reg = @$res[0]['id'];
if(@count($res) > 0 and $id != $id_reg){
    echo 'Nome já Cadastrado!';
    exit();
}
   
if($id == ""){
$query = $pdo->prepare("INSERT INTO $tabela SET nome = :nome, comissao = :comissao");
}else{
    $query = $pdo->prepare("UPDATE $tabela SET nome = :nome, comissao = :comissao where id = '$id'"); 
}
 $query->bindValue(":nome", "$nome");
 $query->bindValue(":comissao", "$comissao");

 $query->execute();

 echo 'Salvo com Sucesso';
?>
<?php
$tabela = 'pacientes';
require_once("../../../conexao.php");

$nome = $_POST['nome'];
$cpf = $_POST['cpf'];
$telefone = $_POST['telefone'];
$endereco = $_POST['endereco'];
$data_nasc = $_POST['data_nasc'];
$tipo_sanguineo = $_POST['tipo_sanguineo'];
$convenio = $_POST['convenio'];
$nome_responsavel = $_POST['nome_responsavel'];
$cpf_responsavel = $_POST['cpf_responsavel'];
$id = $_POST['id'];


//validação cpf
$query = $pdo->query("SELECT * from $tabela where cpf = '$cpf'");    
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$id_reg = @$res[0]['id'];
if(@count($res) > 0 and $id != $id_reg){
    echo 'CPF já Cadastrado!';
    exit();
}

if($id == ""){
$query = $pdo->prepare("INSERT INTO $tabela SET nome = :nome, cpf = :cpf, 
    telefone = :telefone, endereco = :endereco, data_nasc = :data_nasc, tipo_sanguineo = :tipo_sanguineo, 
    data_cad = curDate(), nome_responsavel = :nome_responsavel, cpf_responsavel = :cpf_responsavel, convenio = :convenio");
}else{
    $query = $pdo->prepare("UPDATE $tabela SET nome = :nome, cpf = :cpf, 
    telefone = :telefone, endereco = :endereco, data_nasc = :data_nasc, tipo_sanguineo = :tipo_sanguineo, 
    nome_responsavel = :nome_responsavel, cpf_responsavel = :cpf_responsavel, convenio = :convenio where id = '$id'"); 
}
 $query->bindValue(":nome", "$nome");
 $query->bindValue(":cpf", "$cpf");
 $query->bindValue(":telefone", "$telefone");
 $query->bindValue(":endereco", "$endereco");
 $query->bindValue(":data_nasc", "$data_nasc");
 $query->bindValue(":tipo_sanguineo", "$tipo_sanguineo");
 $query->bindValue(":nome_responsavel", "$nome_responsavel");
 $query->bindValue(":cpf_responsavel", "$cpf_responsavel");
 $query->bindValue(":convenio", "$convenio");
 $query->execute();

 echo 'Salvo com Sucesso';
?>
<?php
    @session_start();
    require_once("conexao.php"); //faz a conexão
    $usuario = $_POST['usuario'];
    $senha = $_POST['senha'];
    $senha_crip = sha1($senha);

    $query = $pdo->prepare("SELECT * from usuarios where email = :email and senha_crip = :senha");
    $query->bindValue(":email", "$usuario");
    $query->bindValue(":senha", "$senha_crip");
    $query->execute();
    $res = $query->fetchAll(PDO::FETCH_ASSOC);
    $linhas = @count($res);
   
    if($linhas > 0){

        if($res[0]['ativo'] != 'Sim'){
            echo '<script>window.alert("Acesso desativado!!")</script>';
            echo '<script>window.location="index.php"</script>';
        }
        $_SESSION['nome'] = $res[0]['nome'];
        $_SESSION['id'] = $res[0]['id'];
        $_SESSION['nivel'] = $res[0]['nivel'];
               

        echo '<script>window.location="painel"</script>';
    }else{
        echo '<script>window.alert("Dados Incorretos")</script>';
        echo '<script>window.location="index.php"</script>';
    }

?>
<?php
 require_once("conexao.php");
 $query = $pdo->query("SELECT * from usuarios");
 $res = $query->fetchAll(PDO::FETCH_ASSOC);
 $linhas = @count($res);
 $senha = '123';
 $senha_crip = md5($senha);
 if($linhas == 0){
    $pdo->query("INSERT INTO usuarios SET nome = '$nome_sistema', email = '$email_sistema', 
    senha = '$senha', senha_crip = '$senha_crip', nivel = 'Administrador', ativo = 'Sim', 
    foto = 'sem-foto.jpg', telefone = '$telefone_sistema', data = curDate()");
 }
?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Clínica Odontológica</title>    
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <link rel="shortcut icon" type="image/x-icon" href="images/icon_logo.png">
    

</head>
<body>   
    <div class="login">
        <div class="form">
           <form method="post" action="autenticar.php">
                <img src="images/logo.png" alt="Logomarca" class="img">
                <input type="email" name="usuario" placeholder="E-mail" required>
                <input type="password" name="senha" placeholder="Senha" required>
               
                <button>Login</button>
                <!-- <a href="cadastro.html" class="btn btn-secundary">Cadastre-se</a><br>
                <a href="#" class="form__action__aside">Esqueci minha senha</a> -->
           </form>
        </div>
    </div>
</body>
</html>
          
<?php
//definir fuso horario
date_default_timezone_set('America/Sao_Paulo');

// conexao banco de dados local
    $servidor = 'localhost';
    $banco = 'clinica';
    $usuario = 'root';
    $senha = '';

    try{
        $pdo = new PDO("mysql:dbname=$banco;host=$servidor;charset=utf8", "$usuario", "$senha");
    }catch(Exception $e){
        echo 'Erro ao conectar ao banco de dados!<br>';
        // echo '<br>';
        echo $e;
    }

    //variáveis globais
    $nome_sistema = 'AM Systems';
    $email_sistema = 'contato@amsystems.com.br';
    $telefone_sistema = "(16)99992-7427";
    $endereco_sistema = "Rua Luiz Leporace, 1236 - Santo Agostinho - Franca(SP)"
    
    
?>
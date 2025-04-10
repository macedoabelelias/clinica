<?php
//definir fuso horario
date_default_timezone_set('America/Sao_Paulo');

$url_sistema = "http://$_SERVER[HTTP_HOST]/"; //busca o local onde está hospedado,ex: www.xxx..
$url = explode("//", $url_sistema);
if($url[1] == 'localhost/'){
	$url_sistema = "http://$_SERVER[HTTP_HOST]/clinica/";
}

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
    
   
//variaveis globais
$nome_sistema = 'AM Systems';
$email_sistema = 'contato@amsystems.com.br';
$telefone_sistema = '(16) 99992-7427';
$endereco_sistema = 'Rua Luiz Leporace, 1236 - Santo Agostinho - Franca (SP)';
$instagram_sistema = 'abelmacedo61';
    

$query = $pdo->query("SELECT * from config");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$linhas = @count($res);
if($linhas == 0){
	$pdo->query("INSERT INTO config SET nome = '$nome_sistema', email = '$email_sistema', 
       telefone = '$telefone_sistema', endereco = '$endereco_sistema', instagram = '$instagram_sistema', 
       logo = 'logo.png', logo_rel = 'logo.jpg', icone = 'icone.png', ativo = 'Sim'");
}else{
    $nome_sistema = $res[0]['nome'];
    $email_sistema = $res[0]['email'];
    $telefone_sistema = $res[0]['telefone'];
    $endereco_sistema = $res[0]['endereco'];
    $instagram_sistema = $res[0]['instagram'];
    $logo_sistema = $res[0]['logo'];
    $logo_rel = $res[0]['logo_rel'];
    $icone_sistema = $res[0]['icone'];
    $ativo_sistema = $res[0]['ativo'];

    if($ativo_sistema != 'Sim' and $ativo_sistema != ''){ ?>
        <style type="text/css">
            @media only screen and (max-width:700px){
                .imgsistema_mobile{
                    width: 300px;
                }
            }
        </style>
        <div style="text-align: center; margin-top: 100px">
            <img src="images/bloqueio.png" class="imgsistema_mobile">
        </div>
    <?php 
    exit();
    } 
} 
?>
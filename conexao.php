<?php 

//definir fuso horário
date_default_timezone_set('America/Sao_Paulo');

//dados conexão bd local
$servidor = 'localhost';
$banco = 'clinica';
$usuario = 'root';
$senha = '';

try {
	$pdo = new PDO("mysql:dbname=$banco;host=$servidor;charset=utf8", "$usuario", "$senha");
} catch (Exception $e) {
	echo 'Erro ao conectar ao banco de dados!<br>';
	echo $e;
}

$url_sistema = "http://$_SERVER[HTTP_HOST]/";
$url = explode("//", $url_sistema);
if($url[1] == 'localhost/'){
	$url_sistema = "http://$_SERVER[HTTP_HOST]/clinica/";
}


//variaveis globais
$nome_sistema = 'MedClin';
$email_sistema = 'contato@mediclin.com.br';
$telefone_sistema = '(16)99992-7427';

$query = $pdo->query("SELECT * from config");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$linhas = @count($res);
if($linhas == 0){
	$pdo->query("INSERT INTO config SET nome = '$nome_sistema', email = '$email_sistema', telefone = '$telefone_sistema', 
	logo = 'logo.png', logo_rel = 'logo.jpg', icone = 'icone.png', marca_dagua = 'Sim', ativo = 'Sim', paciente_receita = 'Sim'");
}else{
$nome_sistema = $res[0]['nome'];
$email_sistema = $res[0]['email'];
$telefone_sistema = $res[0]['telefone'];
$endereco_sistema = $res[0]['endereco'];
$logo_sistema = $res[0]['logo'];
$logo_rel = $res[0]['logo_rel'];
$icone_sistema = $res[0]['icone'];
$telefone_fixo = $res[0]['telefone_fixo'];
$comissao_sistema = $res[0]['comissao'];
$token = $res[0]['token'];
$instancia = $res[0]['instancia'];
$horas_confirmacao = $res[0]['horas_confirmacao'];
$marca_dagua = $res[0]['marca_dagua'];
$ativo_sistema = $res[0]['ativo'];
$paciente_receita = $res[0]['paciente_receita'];

$horas_confirmacaoF = $horas_confirmacao.':00:00';

if($ativo_sistema != 'Sim' and $ativo_sistema != ''){ ?>
	<style type="text/css">
		@media only screen and (max-width: 700px) {
		  .imgsistema_mobile{
		    width:300px;
		  }    
		}
	</style>
	<div style="text-align: center; margin-top: 100px">
	<img src="<?php echo $url_sistema ?>painel/imgages/bloqueio.png" class="imgsistema_mobile">	
	</div>
<?php 
exit();
} 

$whatsapp_sistema = '55'.preg_replace('/[ ()-]+/' , '' , $telefone_sistema);

}	
 ?>

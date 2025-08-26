<?php 
include('../../conexao.php');

setlocale(LC_TIME, 'pt_BR', 'pt_BR.utf-8', 'pt_BR.utf-8', 'portuguese');
date_default_timezone_set('America/Sao_Paulo');
$data_hoje = utf8_encode(strftime('%A, %d de %B de %Y', strtotime('today')));

$id = $_GET['id'];
$dataInicial = @$_GET['dataInicial'];
$dataFinal = @$_GET['dataFinal'];
$obs = @$_GET['obs'];
$motivo = @$_GET['motivo'];
$id_usuario = @$_GET['id_usuario'];

$query2 = $pdo->query("SELECT * FROM usuarios where id = '$id_usuario' order by id asc");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
$nome_medico = $res2[0]['nome'];

$dataInicialF = implode('/', array_reverse(explode('-', $dataInicial)));
$dataFinalF = implode('/', array_reverse(explode('-', $dataFinal)));	

$datas = "";
if($dataInicial == $dataFinal){
	$datas = $dataInicialF;
}else{
	$datas = $dataInicialF.' até '.$dataFinalF;
}

$query2 = $pdo->query("SELECT * FROM pacientes where id = '$id'");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
if(@count($res2) > 0){
	$nome_paciente = $res2[0]['nome'];
	$telefone_paciente = $res2[0]['telefone'];	
	$nome_paciente = $res2[0]['nome'];
	$endereco_paciente = $res2[0]['endereco'];
	$data_nasc = $res2[0]['data_nasc'];
	$tipo_sanguineo = $res2[0]['tipo_sanguineo'];
	$nome_responsavel = $res2[0]['nome_responsavel'];
	$convenio = $res2[0]['convenio'];
	$sexo = $res2[0]['sexo'];
	$obs_paciente = $res2[0]['obs'];
	$cpf_paciente = $res2[0]['cpf'];
	$cpf_responsavel = $res2[0]['cpf_responsavel'];
	$profissao = $res2[0]['profissao'];
	$estado_civil = $res2[0]['estado_civil'];

	//idade do paciente
	// separando yyyy, mm, ddd
    list($ano, $mes, $dia) = explode('-', $data_nasc);
    // data atual
    $hoje = mktime(0, 0, 0, date('m'), date('d'), date('Y'));
    // Descobre a unix timestamp da data de nascimento do fulano
    $nascimento = mktime( 0, 0, 0, $mes, $dia, $ano);
    // cálculo
    $idade = floor((((($hoje - $nascimento) / 60) / 60) / 24) / 365.25);

    
	$data_nascF = implode('/', array_reverse(explode('-', $data_nasc)));
	
	$query2 = $pdo->query("SELECT * from convenios where id = '$convenio'");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
$linhas2 = @count($res2);
if($linhas2 > 0){
	$nome_convenio = $res2[0]['nome'];
}else{
	$nome_convenio = 'Particular';
}

}


?>
<!DOCTYPE html>
<html>
<head>

<style>

@import url('https://fonts.cdnfonts.com/css/tw-cen-mt-condensed');
@page { margin: 145px 20px 25px 20px; }
#header { position: fixed; left: 0px; top: -110px; bottom: 100px; right: 0px; height: 35px; text-align: center; padding-bottom: 100px; }
#content {margin-top: 0px;}
#footer { position: fixed; left: 0px; bottom: -60px; right: 0px; height: 80px; }
#footer .page:after {content: counter(page, my-sec-counter);}
body {font-family: 'Tw Cen MT', sans-serif;}

.marca{
	position:fixed;
	left:50;
	top:130;
	width:80%;
	opacity:10%;
}

</style>

</head>
<body>
<?php 
if($marca_dagua == 'Sim'){ ?>
<img class="marca" src="<?php echo $url_sistema ?>img/logo.jpg">	
<?php } ?>


<div id="header" >

	<div style="border-style: solid; font-size: 10px; height: 50px;">
		<table style="width: 100%; border: 0px solid #ccc;">
			<tr>
				<td style="border: 1px; solid #000; width: 20%; text-align: left;">
					<img style="margin-top: 5px; margin-left: 7px;" id="imag" src="<?php echo $url_sistema ?>img/logo.jpg" width="140px">
				</td>
				<td style="width: 20%; text-align: left; font-size: 13px;">
				
				</td>
				<td style="width: 5%; text-align: center; font-size: 13px;">
				
				</td>
				<td style="width: 55%; text-align: right; font-size: 9px;padding-right: 10px;">
						<b><big>ATESTADO MÉDICO</big></b><br>

						<br>
						 <?php echo mb_strtoupper($data_hoje) ?>
				</td>
			</tr>		
		</table>
	</div>

<br>

		

		
		<div align="center" style="margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #000; font-size:17px"><b>ATESTADO MÉDICO</b></div>


</div>

<div id="footer" class="row">
<hr style="margin-bottom: 0;">
	<table style="width:100%;">
		<tr style="width:100%;">
			<td style="width:60%; font-size: 10px; text-align: left;"><?php echo $nome_sistema ?> / Telefone: <?php echo $telefone_sistema ?> / Email: <?php echo $email_sistema ?></td>
			<td style="width:40%; font-size: 10px; text-align: right;"><p class="">  </p></td>
		</tr>
	</table>
</div>

<div id="content" style="margin-top: 70px;">

<div style="font-size: 15px;">
	Atesto para os devidos fins que o Sr(a) <b><?php echo $nome_paciente ?></b> portador do CPF <?php echo $cpf_paciente ?> esteve sob cuidados médicos no dia <?php echo $data_hoje ?> e deverá se afastar de suas atividades pelo período de <b><?php echo $datas ?></b> por motivo de <?php echo $motivo ?>
</div>

<?php if($obs != ""){ ?>
<div style="margin-top: 20px; border:1px solid #000; font-size: 14px; padding:5px">
	<b>Informações Relevantes</b>
	<p style="font-size: 13px"><?php echo $obs ?></p>

</div>
<?php } ?>

 <div style="margin-top: 80px; font-size:13px" align="center">
 	__________________________________________________
 	<br>Dr <?php echo $nome_medico ?>
 </div>
</div>
	

</body>

</html>



<?php 
include('../../conexao.php');

setlocale(LC_TIME, 'pt_BR', 'pt_BR.utf-8', 'pt_BR.utf-8', 'portuguese');
date_default_timezone_set('America/Sao_Paulo');
$data_hoje = utf8_encode(strftime('%A, %d de %B de %Y', strtotime('today')));

$id = $_GET['id'];
$id_paciente = $_GET['id'];
$anamnese = $_GET['anamnese'];
$historico = $_GET['historico'];

$limite = 1000;
if($historico == ""){
	$limite = 1000;
}

if($historico != "" and $historico != "Não"){
	$limite = $historico;
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
						<b><big>FICHA DO PACIENTE</big></b><br>

						<br>
						 <?php echo mb_strtoupper($data_hoje) ?>
				</td>
			</tr>		
		</table>
	</div>

<br>

		<table id="" style="border-style: solid; font-size: 9px; margin-bottom:10px; width: 100%; table-layout: fixed; margin-top:10px;">
			<thead>
				
				<tr id="cabeca" style="margin-left: 0px; background-color:#f2f0f0">
					<td colspan="8" style="width:100%; font-size: 10px"><b>DADOS DO PACIENTE</b> </td>					
				</tr>
				<tr >
					<td style="width:5%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">NOME: </td>
					<td style="width:35%; border-right: : 1px solid #000; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($nome_paciente) ?>
					</td>
					
					<td style="width:5%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">CPF: </td>
					<td style="width:13%; border-bottom: : 1px solid #000; border-right: 1px solid #000;">
						<?php echo mb_strtoupper($cpf_paciente) ?>
					</td>


					<td style="width:9%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">TELEFONE: </td>
					<td style="width:13%; border-bottom: : 1px solid #000; border-right: 1px solid #000;">
						<?php echo mb_strtoupper($telefone_paciente) ?>
					</td>

					<td style="width:5%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">SEXO: </td>
					<td style="width:5%; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($sexo) ?>
					</td>
    			</tr>


    			<tr >
					<td style="width:8%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">CONVÊNIO: </td>
					<td style="width:30%; border-right: : 1px solid #000; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($nome_convenio) ?>
					</td>
					
					<td style="width:5%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">IDADE: </td>
					<td style="width:11%; border-bottom: : 1px solid #000; border-right: 1px solid #000;">
						<?php echo mb_strtoupper($idade) ?> Anos
					</td>


					<td style="width:10%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">NASCIMENTO: </td>
					<td style="width:13%; border-bottom: : 1px solid #000; border-right: 1px solid #000;">
						<?php echo mb_strtoupper($data_nascF) ?>
					</td>

					<td style="width:13%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">TIPO SANGUÍNEO: </td>
					<td style="width:5%; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($tipo_sanguineo) ?>
					</td>
    			</tr>


    			<tr >
					<td style="width:8%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">PROFISSÃO </td>
					<td colspan="3" style="width:30%; border-right: : 1px solid #000; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($profissao) ?>
					</td>
					
					


					<td style="width:10%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">ESTADO CIVIL: </td>
					<td colspan="3" style="width:13%; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($estado_civil) ?>
					</td>

					
    			</tr>


    			<tr >
					<td style="width:8%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">OBS </td>
					<td colspan="3" style="width:30%; border-right: : 1px solid #000; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($obs_paciente) ?>
					</td>
					
					


					<td style="width:10%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">ENDEREÇO: </td>
					<td colspan="3" style="width:13%; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($endereco_paciente) ?>
					</td>

					
    			</tr>


    			<?php if($nome_responsavel != ""){ ?>
    				<tr >
					<td style="width:8%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">RESP </td>
					<td colspan="3" style="width:30%; border-right: : 1px solid #000; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($nome_responsavel) ?>
					</td>
					
					


					<td style="width:10%; border-right: 1px solid #000;border-bottom: : 1px solid #000;">CPF RESP: </td>
					<td colspan="3" style="width:13%; border-bottom: : 1px solid #000;">
						<?php echo mb_strtoupper($cpf_responsavel) ?>
					</td>

					
    			</tr>

    			<?php } ?>
    			
			</thead>
		</table>

		<?php 
			$query = $pdo->query("SELECT * FROM historico_paciente where paciente = '$id' order by id desc limit $limite");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$total_reg = @count($res);
if($total_reg > 0 and $historico != "Não"){
		 ?>
		<div align="left" style="margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #000; font-size:12px"><b>HISTÓRICO CLÍNICO</b></div>

<?php } ?>


</div>

<div id="footer" class="row">
<hr style="margin-bottom: 0;">
	<table style="width:100%;">
		<tr style="width:100%;">
			<td style="width:60%; font-size: 10px; text-align: left;"><?php echo $nome_sistema ?> / Telefone: <?php echo $telefone_sistema ?> / Email: <?php echo $email_sistema ?></td>
			<td style="width:40%; font-size: 10px; text-align: right;"><p class="page">Página  </p></td>
		</tr>
	</table>
</div>

<div id="content" style="margin-top: 0;">
	<?php 
		$query = $pdo->query("SELECT * FROM historico_paciente where paciente = '$id' order by id desc limit $limite");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$total_reg = @count($res);
if($total_reg > 0 and $historico != "Não"){
	 ?>

		<table style="width: 100%; table-layout: fixed; font-size:10px; margin-top: 105px">
			<thead>
				<tbody>
					<?php 

for($i=0; $i < $total_reg; $i++){
	
	$descricao = $res[$i]['descricao'];
	$data = $res[$i]['data'];
	$consulta = $res[$i]['consulta'];
	$funcionario = $res[$i]['funcionario'];
	$nome_funcionario = $res[$i]['nome_funcionario'];

	$dataF = implode('/', array_reverse(explode('-', $data)));

	
  	 ?>

  	 
      <tr style="">
<td style="width:100%; border-bottom:1px solid #919191; padding-bottom: 5px">
<span style="color:#096385; font-size: 10px"><i>Dr <?php echo $nome_funcionario ?></i> <span style="color:#360202; font-size: 9px">(<?php echo $dataF ?>)</span></span><br>
<span style="color:#363636; font-size: 9px; " >
	<i>"<?php echo $descricao ?>"</i>
	</span>
</td>


    </tr>

<?php }  ?>
				</tbody>
	
			</thead>
		</table>
	
<?php }else{ echo '<div style="margin-top:60px"></div>'; }  ?>

</div>
	
	<?php if($anamnese != 'Não'){ ?>
	<div style="margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #000; font-size:12px"><b>ANAMNESE</b></div>

	<?php 

	$total_itens = 0;

$query = $pdo->query("SELECT * FROM grupo_ana ORDER BY id asc");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$total_reg = @count($res);
if($total_reg > 0){
for($i=0; $i < $total_reg; $i++){
$id_grupo = $res[$i]['id'];
$nome_grupo = $res[$i]['nome'];

	$query2 = $pdo->query("SELECT * FROM anamnese where paciente = '$id_paciente' and grupo = '$id_grupo' ");
		$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
		$total_reg2 = @count($res2);
		if($total_reg2 > 0){
			$total_itens += 1;
			echo '<div style="color:red; font-size:12px; margin-bottom:5px"><b>'.$nome_grupo.'</b></div>
			<div style="margin-bottom:10px; border-bottom:1px solid #383838; display: flex;">';
			for($i2=0; $i2 < $total_reg2; $i2++){
			
			
			$descricao_ana = $res2[$i2]['descricao'];
			$item = $res2[$i2]['item'];

			$query3 = $pdo->query("SELECT * FROM itens_ana where id = '$item'");
$res3 = $query3->fetchAll(PDO::FETCH_ASSOC);
$nome = $res3[0]['nome'];					
		if($anamnese == 1){
			echo '
			<div> ';
		}else{
			echo '
		<div style="display:inline-block; width:48%;">';
		}
		echo '
		<img width="10px" src="'.$url_sistema.'img/check.jpg">	
		<label class="labelcheck" style="font-size:11px"><b>
		'.$nome.'
		</b></label>
		<span style="margin-left:3px; font-size:11px">'.$descricao_ana.'</span>
		</div>
		';

							} echo '</div>'; } } } 




if($total_itens == 0){
	echo '<span style="font-size:13px">Nenhuma Anamnese Lançada!</span>';
} ?>
<?php } ?>

</body>

</html>



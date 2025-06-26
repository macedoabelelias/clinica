<?php 
$tabela = 'agendamentos';
require_once("../../../conexao.php");
$id = $_POST['id'];

$query = $pdo->query("SELECT * from $tabela where paciente = '$id' order by id desc");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$linhas = @count($res);
if($linhas > 0){
echo <<<HTML
<small>
	<table class="table table-hover" id="tabela2">
	<thead> 
	<tr> 
	<th>Procedimento</th>	
	<th class="esc">Data</th>	
	<th class="esc">Médico</th>	
	<th class="esc">Convênio</th>
	<th class="esc">Status</th>
	
	</tr> 
	</thead> 
	<tbody>	
HTML;


for($i=0; $i<$linhas; $i++){
	$id = $res[$i]['id'];
	$procedimento = $res[$i]['servico'];
	$funcionario = $res[$i]['funcionario'];
	$data = $res[$i]['data'];	
	$convenio = $res[$i]['convenio'];	
	$valor = $res[$i]['valor'];
	$status = $res[$i]['status'];

	$dataF = implode('/', array_reverse(explode('-', $data)));
	$valorF = number_format($valor, 2, ',', '.');

	$query2 = $pdo->query("SELECT * from convenios where id = '$convenio'");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
$linhas2 = @count($res2);
if($linhas2 > 0){
	$nome_convenio = $res2[0]['nome'];
	$valorFormat = '';
}else{
	$nome_convenio = 'Particular';
	$valorFormat = '(R$ '.$valorF.')';
}

$query2 = $pdo->query("SELECT * FROM procedimentos where id = '$procedimento'");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
if(@count($res2) > 0){
	$nome_serv = $res2[0]['nome'];	
}else{
	$nome_serv = 'Não Lançado';	
}

$query2 = $pdo->query("SELECT * FROM usuarios where id = '$funcionario'");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
if(@count($res2) > 0){
	$nome_medico = $res2[0]['nome'];	
}else{
	$nome_medico = 'Não Lançado';	
}


if($status == 'Agendado'){		
	$imagemClasse = 'red';		
}else if($status == 'Finalizado'){	
	$imagemClasse = 'green';	
}else if($status == 'Confirmado'){
	$imagemClasse = 'blue';
	}

echo <<<HTML
<tr>
<td>{$nome_serv}</td>
<td class="esc">{$dataF}</td>
<td class="esc">{$nome_medico}</td>
<td class="esc">{$nome_convenio} <span class="text-danger"><small>{$valorFormat}</small></span></td>
<td class="esc"><div style="color:#FFF; background:{$imagemClasse}; padding:0px; width:75px; text-align: center; font-size: 12px; ">{$status}</div></td>

</tr>
HTML;

}


echo <<<HTML
</tbody>
<small><div align="center" id="mensagem-excluir"></div></small>
</table>
HTML;

}else{
	echo '<small>Nenhuma consulta Encontrada!</small>';
}
?>



<script type="text/javascript">
	$(document).ready( function () {		
    $('#tabela2').DataTable({
    	"language" : {
            //"url" : '//cdn.datatables.net/plug-ins/1.13.2/i18n/pt-BR.json'
        },
        "ordering": false,
		"stateSave": true
    });
} );
</script>


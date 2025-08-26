<?php 
require_once("../../../conexao.php");
$tabela = 'historico_paciente';
$data_hoje = date('Y-m-d');

@session_start();
$id_usuario = $_SESSION['id'];

$id_pac = @$_POST['id'];

$query = $pdo->query("SELECT * FROM $tabela where paciente = '$id_pac' order by id desc");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$total_reg = @count($res);
if($total_reg > 0){
	for($i=0; $i < $total_reg; $i++){	
	$id = $res[$i]['id'];
	$descricao = $res[$i]['descricao'];
	$data = $res[$i]['data'];
	$consulta = $res[$i]['consulta'];
	$funcionario = $res[$i]['funcionario'];
	$nome_funcionario = $res[$i]['nome_funcionario'];

	$dataF = implode('/', array_reverse(explode('-', $data)));

	$ocultar_excluir = '';
	if($funcionario != $id_usuario){
		$ocultar_excluir = 'ocultar';
	}

	echo <<<HTML
	<div style="border-bottom:1px solid #919191; padding-bottom: 5px">
	<span style="color:#096385; font-size: 13px"><i>Dr {$nome_funcionario}</i> <span style="color:#360202; font-size: 11px">({$dataF})</span></span>

	<li class="dropdown head-dpdn2" style="display: inline-block;">
		<a title="Remover Descrição" href="#" class="dropdown-toggle {$ocultar_excluir}" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-times text-danger"></i></a>

		<ul class="dropdown-menu" style="margin-left:-100px;">
		<li>
		<div class="notification_desc2">
		<p>Confirmar Exclusão? <a href="#" onclick="excluirHistorico('{$id}', '{$id_pac}')"><span class="text-danger">Sim</span></a></p>
		</div>
		</li>										
		</ul>
		</li>

	<br>
	<span style="color:#363636; font-size: 12px">
	<i>"{$descricao}"</i>
	</span>
	</div>
	HTML;

	}
}else{
	echo '<small>Nenhum Histórico Lançado!</small>';
}



?>

<script type="text/javascript">
	function excluirHistorico(id, paciente){	
        
    $.ajax({
        url: 'paginas/' + pag + "/excluir_historico.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(mensagem){
             
            if (mensagem.trim() == "Excluído com Sucesso") {  

                listarHistorico(paciente);
            } 
        }
    });
}
</script>
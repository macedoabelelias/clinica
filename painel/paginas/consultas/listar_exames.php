<?php 
require_once("../../../conexao.php");
$tabela = 'exames';
$data_hoje = date('Y-m-d');

@session_start();
$id_usuario = $_SESSION['id'];

$id_pac = @$_POST['id'];

$query = $pdo->query("SELECT * FROM $tabela where paciente = '$id_pac' order by id asc");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$total_reg = @count($res);
if($total_reg > 0){
	for($i=0; $i < $total_reg; $i++){	
	$id = $res[$i]['id'];
	$exame = $res[$i]['exame'];
	$clinica = $res[$i]['clinica'];
	if($clinica == 'Sim'){
		$classe = '';
	}else{
		$classe = '(Fora da Clínica)';
	}

	echo <<<HTML
	<div style="margin-top: 10px">
	<span style="font-size: 15px"><i class="fa fa-check text-success"></i> <b>{$exame}</b> <span style="font-size: 12px; color:#400303">{$classe}</span>

	<li class="dropdown head-dpdn2" style="display: inline-block;">
		<a title="Remover Descrição" href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-times text-danger"></i></a>

		<ul class="dropdown-menu" style="margin-left:-100px;">
		<li>
		<div class="notification_desc2">
		<p>Confirmar Exclusão? <a href="#" onclick="excluirExame('{$id}', '{$id_pac}')"><span class="text-danger">Sim</span></a></p>
		</div>
		</li>										
		</ul>
		</li>

	<br>
	
	</div>
	HTML;

	}
}else{
	echo '<small>Nenhum Exame Lançado!</small>';
}



?>

<script type="text/javascript">
	function excluirExame(id, paciente){	
        
    $.ajax({
        url: 'paginas/' + pag + "/excluir_exame.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(mensagem){
             
            if (mensagem.trim() == "Excluído com Sucesso") {  

                listarExames(paciente);
                limparCamposExame();
            } 
        }
    });
}


</script>
<?php 
$tabela = 'pacientes';
require_once("../../../conexao.php");

$query = $pdo->query("SELECT * from $tabela order by id desc");
$res = $query->fetchAll(PDO::FETCH_ASSOC);
$linhas = @count($res);
if($linhas > 0){
echo <<<HTML
<small>
	<table class="table table-hover" id="tabela">
	<thead> 
	<tr> 
	<th>Nome</th>	
	<th class="esc">Idade</th>	
	<th class="esc">Profissão</th>	
	<th class="esc">Nascimento</th>
	<th class="esc">Convênio</th>
	<th class="esc">Tipo Sanguíneo</th>		
	<th>Ações</th>
	</tr> 
	</thead> 
	<tbody>	
HTML;


for($i=0; $i<$linhas; $i++){
	$id = $res[$i]['id'];
	$nome = $res[$i]['nome'];
	$telefone = $res[$i]['telefone'];
	$cpf = $res[$i]['cpf'];	
	$endereco = $res[$i]['endereco'];	
	$data_cad = $res[$i]['data_cad'];
	$data_nasc = $res[$i]['data_nasc'];	
	$convenio = $res[$i]['convenio'];
	$tipo_sanguineo = $res[$i]['tipo_sanguineo'];
	$nome_responsavel = $res[$i]['nome_responsavel'];
	$cpf_responsavel = $res[$i]['cpf_responsavel'];
	$sexo = $res[$i]['sexo'];
	$obs = $res[$i]['obs'];
	$estado_civil = $res[$i]['estado_civil'];
	$profissao = $res[$i]['profissao'];

	$tel_pessoaF = '55'.preg_replace('/[ ()-]+/' , '' , $telefone);

	$data_nascF = implode('/', array_reverse(explode('-', $data_nasc)));
	$data_cadF = implode('/', array_reverse(explode('-', $data_cad)));

	$query2 = $pdo->query("SELECT * from convenios where id = '$convenio'");
$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
$linhas2 = @count($res2);
if($linhas2 > 0){
	$nome_convenio = $res2[0]['nome'];
}else{
	$nome_convenio = 'Nenhum';
}

//idade do paciente
	// separando yyyy, mm, ddd
    list($ano, $mes, $dia) = explode('-', $data_nasc);
    // data atual
    $hoje = mktime(0, 0, 0, date('m'), date('d'), date('Y'));
    // Descobre a unix timestamp da data de nascimento do fulano
    $nascimento = mktime( 0, 0, 0, $mes, $dia, $ano);
    // cálculo
    $idade = floor((((($hoje - $nascimento) / 60) / 60) / 24) / 365.25);


echo <<<HTML
<tr>
<td>
<input type="checkbox" id="seletor-{$id}" class="form-check-input" onchange="selecionar('{$id}')">
{$nome}
</td>
<td class="esc">{$idade} anos</td>
<td class="esc">{$profissao}</td>
<td class="esc">{$data_nascF}</td>
<td class="esc">{$nome_convenio}</td>
<td class="esc">{$tipo_sanguineo}</td>
<td>
	<big><a href="#" onclick="editar('{$id}','{$nome}','{$telefone}','{$cpf}','{$endereco}','{$data_nasc}','{$tipo_sanguineo}','{$nome_responsavel}','{$cpf_responsavel}','{$convenio}','{$sexo}','{$obs}','{$estado_civil}','{$profissao}')" title="Editar Dados"><i class="fa fa-edit text-primary"></i></a></big>

	<li class="dropdown head-dpdn2" style="display: inline-block;">
		<a href="#" class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><big><i class="fa fa-trash-o text-danger"></i></big></a>

		<ul class="dropdown-menu" style="margin-left:-230px;">
		<li>
		<div class="notification_desc2">
		<p>Confirmar Exclusão? <a href="#" onclick="excluir('{$id}')"><span class="text-danger">Sim</span></a></p>
		</div>
		</li>										
		</ul>
</li>

<big><a href="#" onclick="mostrar('{$nome}','{$telefone}','{$endereco}','{$data_nascF}','{$tipo_sanguineo}','{$nome_responsavel}', '{$nome_convenio}', '{$sexo}','{$obs}','{$idade}','{$id}','{$profissao}','{$estado_civil}','{$cpf}')" title="Mostrar Dados"><i class="fa fa-info-circle text-primary"></i></a></big>


	<big><a href="#" onclick="arquivo('{$id}', '{$nome}')" title="Inserir / Ver Arquivos"><i class="fa fa-file-o " style="color:#22146e"></i></a></big>

	<big><a href="#" onclick="fichaPersonalizada('{$id}', '{$nome}')" title="Ficha Personalizada"><i class="fa fa-file-pdf-o " style="color:red"></i></a></big>


	<big><a href="#" onclick="consultas('{$id}', '{$nome}')" title="Últimas Consultas"><i class="fa fa-stethoscope text-success"></i></a></big>

	<big><a href="#" onclick="anamnese('{$id}', '{$nome}')" title="Editar Anamnese"><i class="fa fa-stethoscope text-primary"></i></a></big>

		<big><a class="" href="http://api.whatsapp.com/send?1=pt_BR&phone={$tel_pessoaF}" title="Whatsapp" target="_blank"><i class="fa fa-whatsapp " style="color:green"></i></a></big>


</td>
</tr>
HTML;

}


echo <<<HTML
</tbody>
<small><div align="center" id="mensagem-excluir"></div></small>
</table>
HTML;

}else{
	echo '<small>Nenhum Registro Encontrado!</small>';
}
?>



<script type="text/javascript">
	$(document).ready( function () {		
    $('#tabela').DataTable({
    	"language" : {
            //"url" : '//cdn.datatables.net/plug-ins/1.13.2/i18n/pt-BR.json'
        },
        "ordering": false,
		"stateSave": true
    });
} );
</script>

<script type="text/javascript">
	function editar(id, nome, telefone, cpf, endereco, data_nasc, tipo_sanguineo, nome_responsavel, cpf_responsavel, convenio, sexo, obs, estado_civil, profissao){
		$('#mensagem').text('');
    	$('#titulo_inserir').text('Editar Registro');

    	$('#id').val(id);
    	$('#nome').val(nome);
    	$('#cpf').val(cpf);
    	$('#telefone').val(telefone);
    	$('#endereco').val(endereco);
    	$('#data_nasc').val(data_nasc);
    	$('#nome_responsavel').val(nome_responsavel);
    	$('#tipo_sanguineo').val(tipo_sanguineo).change();
    	$('#convenio').val(convenio).change();
    	$('#cpf_responsavel').val(cpf_responsavel);
    	$('#cpf').val(cpf);
    	$('#sexo').val(sexo).change();
    	$('#obs').val(obs);
    	$('#estado_civil').val(estado_civil);
    	$('#profissao').val(profissao);

    	$('#modalForm').modal('show');
	}


	function mostrar(paciente, telefone, endereco, data_nasc, tipo_sanguineo, nome_responsavel, nome_convenio, sexo, obs_paciente, idade, id_paciente, profissao, estado_civil, cpf){

		if(nome_responsavel == ""){
			$('#responsavel_div').hide();
		}else{
			$('#responsavel_div').show();
		}

		if(obs_paciente == ""){
			$('#obs_div').hide();
		}else{
			$('#obs_div').show();
		}

		if(profissao == ""){
			profissao = 'Nenhuma!';
		}


		
		$('#nome_dados').text(paciente);
		$('#cpf_dados').text(cpf);
		$('#idade_dados').text(idade + ' anos');
		$('#telefone_dados').text(telefone);	
		$('#data_nasc_dados').text(data_nasc);
		$('#tipo_dados').text(tipo_sanguineo);
		$('#sexo_dados').text(sexo);
		$('#convenio_dados').text(nome_convenio);
		$('#endereco_dados').text(endereco);

		$('#responsavel_dados').text(nome_responsavel);	
		$('#obs_dados').text(obs_paciente);
		$('#profissao_dados').text(profissao);
		$('#estado_civil_dados').text(estado_civil);

		
		$('#id_pac').val(id_paciente);

		$('#modalDados').modal('show');
		listarHistorico(id_paciente);
		listarAnaPac(id_paciente);
	}

	function limparCampos(){
		$('#id').val('');
    	$('#nome').val('');
    	$('#cpf').val('');
    	$('#telefone').val('');
    	$('#endereco').val('');
    	$('#data_nasc').val('');
    	$('#nome_responsavel').val('');
    	$('#cpf_responsavel').val('');
    	$('#obs').val('');


    	$('#ids').val('');
    	$('#btn-deletar').hide();	
	}

	function selecionar(id){

		var ids = $('#ids').val();

		if($('#seletor-'+id).is(":checked") == true){
			var novo_id = ids + id + '-';
			$('#ids').val(novo_id);
		}else{
			var retirar = ids.replace(id + '-', '');
			$('#ids').val(retirar);
		}

		var ids_final = $('#ids').val();
		if(ids_final == ""){
			$('#btn-deletar').hide();
		}else{
			$('#btn-deletar').show();
		}
	}

	function deletarSel(){
		var ids = $('#ids').val();
		var id = ids.split("-");
		
		for(i=0; i<id.length-1; i++){
			excluir(id[i]);			
		}

		limparCampos();
	}



		function arquivo(id, nome){
    $('#id-arquivo').val(id);    
    $('#nome-arquivo').text(nome);
    $('#modalArquivos').modal('show');
    $('#mensagem-arquivo').text(''); 
    listarArquivos();   
}


function listarHistorico(id){
	pag = 'consultas';
	$.ajax({
        url: 'paginas/' + pag + "/listar_historico.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(result){
            $("#historico_div").html(result);
            
        }
    });
}

function anamnese(paciente, nome){
		$('#id_pac_ana').val(paciente);	
		$('#nome_anamnese').text(nome);	
		$('#modalAnamnese').modal('show');
		listarAnamnese(paciente);
}


function fichaPersonalizada(paciente, nome){
		$('#id_ficha').val(paciente);	
		$('#nome_ficha').text(nome);	
		$('#modalFicha').modal('show');
		
}

function consultas(paciente, nome){			
		$('#nome_consulta').text(nome);	
		$('#modalConsultas').modal('show');
		listarConsultas(paciente)
}

function listarConsultas(id){	
	$.ajax({
        url: 'paginas/' + pag + "/listar_consultas.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(result){
            $("#listar_consultas").html(result);            
        }
    });
}
	
</script>
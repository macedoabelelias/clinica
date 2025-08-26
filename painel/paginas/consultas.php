<?php 
@session_start();
require_once("verificar.php");
require_once("../conexao.php");

$pag = 'consultas';



$data_hoje = date('Y-m-d');
$data_ontem = date('Y-m-d', strtotime("-1 days",strtotime($data_hoje)));

$mes_atual = Date('m');
$ano_atual = Date('Y');
$data_inicio_mes = $ano_atual."-".$mes_atual."-01";

if($mes_atual == '4' || $mes_atual == '6' || $mes_atual == '9' || $mes_atual == '11'){
	$dia_final_mes = '30';
}else if($mes_atual == '2'){
	$dia_final_mes = '28';
}else{
	$dia_final_mes = '31';
}

$data_final_mes = $ano_atual."-".$mes_atual."-".$dia_final_mes;

$id_func = $_SESSION['id'];

//verificar se ele tem a permissão de estar nessa página
if(@$consultas == 'ocultar'){
    echo "<script>window.location='../index.php'</script>";
    exit();
}
?>

<div class="bs-example widget-shadow" style="padding:15px">

	<div class="row">
		<div class="col-md-5" style="margin-bottom:5px;">
			<div style="float:left; margin-right:10px"><span><small><i title="Data de Vencimento Inicial" class="fa fa-calendar-o"></i></small></span></div>
			<div  style="float:left; margin-right:20px">
				<input type="date" class="form-control " name="data-inicial"  id="data-inicial-caixa" value="<?php echo $data_hoje ?>" required>
			</div>

			<div style="float:left; margin-right:10px"><span><small><i title="Data de Vencimento Final" class="fa fa-calendar-o"></i></small></span></div>
			<div  style="float:left; margin-right:30px">
				<input type="date" class="form-control " name="data-final"  id="data-final-caixa" value="<?php echo $data_hoje ?>" required>
			</div>
		</div>


		<div class="col-md-2" align="center">	
			<div > 
				<small >
					<a title="Conta de Ontem" class="text-muted" href="#" onclick="valorData('<?php echo $data_ontem ?>', '<?php echo $data_ontem ?>')"><span>Ontem</span></a> / 
					<a title="Conta de Hoje" class="text-muted" href="#" onclick="valorData('<?php echo $data_hoje ?>', '<?php echo $data_hoje ?>')"><span>Hoje</span></a> / 
					<a title="Conta do Mês" class="text-muted" href="#" onclick="valorData('<?php echo $data_inicio_mes ?>', '<?php echo $data_final_mes ?>')"><span>Mês</span></a>
				</small>
			</div>
		</div>



	<div class="col-md-5"  align="center">	
			<div > 
				<small >
					<a title="Status das Consultas" class="text-muted" href="#" onclick="buscarContas('')"><span>Todas</span></a> / 
					<a title="Agendado" class="text-danger" href="#" onclick="buscarContas('Agendado')"><span>Agendadas</span></a> / 
					<a title="Confirmado" class="text-primary" href="#" onclick="buscarContas('Confirmado')"><span>Confirmadas</span></a> / 
					<a title="Finalizado" class="verde" href="#" onclick="buscarContas('Finalizado')"><span>Finalizadas</span></a>
				</small>
			</div>
		</div>	


				

		<input type="hidden" id="buscar-contas">

	</div>

	

	<hr>
	<div id="listar">

	</div>
	
</div>





<!-- Modal Dados-->
<div class="modal fade" id="modalDados" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-lg" role="document">
		<div class="modal-content ">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_dados"></span> <span style="margin-left: 25px; font-size: 15px"><a title="PDF da Ficha Paciente" href="" onclick="ficha()"><i class="fa fa-file-pdf-o text-danger"></i> Imprimir Ficha</a></span></h4>
				<button id="btn-fechar-perfil" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -20px">
					<span aria-hidden="true" >&times;</span>
				</button>
			</div>
			
			<div class="modal-body">

				<div class="row">
					<div class="col-md-7" style="font-size:14px">
						<div style="margin-bottom: 5px; border-bottom:1px solid #cecece; padding-bottom:3px">		
							<span style="margin-right: 20px"><b>Idade</b> <span id="idade_dados"></span></span>			
						<span style="margin-right: 20px"><b>Telefone</b> <span id="telefone_dados"></span></span>
						<span style=""><b>Nascimento</b> <span id="data_nasc_dados"></span></span>
						</div>



						<div style="margin-bottom: 5px; border-bottom:1px solid #cecece; padding-bottom:3px">			
							<span style="margin-right: 20px"><b>Tipo Sanguíneo</b> <span id="tipo_dados"></span></span>			
						<span style="margin-right: 20px"><b>Sexo</b> <span id="sexo_dados"></span></span>
						<span style=""><b>Convênio</b> <span id="convenio_dados"></span></span>
						</div>


						<div style="margin-bottom: 5px; border-bottom:1px solid #cecece; padding-bottom:3px">			
							<span id="responsavel_div" style="margin-right: 20px"><b>Responsável</b> <span id="responsavel_dados"></span></span>							

						<span id="obs_div" style="margin-right: 20px"><b>OBS</b> <span id="obs_dados"></span></span>
						
						</div>


						<div style="margin-bottom: 5px; border-bottom:1px solid #cecece; padding-bottom:3px">		
							<span style="margin-right: 20px"><b>Endereço</b> <span id="endereco_dados"></span></span>
						
						</div>

							<div style="margin-bottom: 5px; border-bottom:1px solid #cecece; padding-bottom:3px">		
							<span style="margin-right: 20px"><b>Estado Cívil</b> <span id="estado_civil_dados"></span></span>

							<span style="margin-right: 20px"><b>Profissão</b> <span id="profissao_dados"></span></span>
						
						</div>

						<div style="margin-top: 15px; margin-bottom: 5px; border-bottom: 1px solid #000"><b>ANAMNESE</b></div>
						<div id="listar_ana_pac" style="margin-top:5px">
							
						</div>

					</div>	

					<div class="col-md-5" style="border-left: 1px solid #242323; font-size:14px" >							
						<b>Histório Clínico</b>	

						<div id="historico_div" style="overflow: scroll; max-height:300px; scrollbar-width: thin; padding:2px">

						</div>


						<div class="row">
							<form id="form-historico">
							<div class="col-md-10">
							<textarea maxlength="2000" name="historico" id="historico" class="form-control" required></textarea>
							</div>
							<div class="col-md-2" style="margin-top: 40px">
								<button type="submit" class="btn btn-sm btn-primary"><i class="fa fa-check"></i></button>
							</div>

							<input type="hidden" name="id_pac" id="id_pac">
							<input type="hidden" name="id_con" id="id_con">
							</form>
						</div>

						<small><div id="mensagem-historico"></div></small>		
					</div>


				</div>





			</div>

			
		</div>
	</div>
</div>



<!-- Modal Anamnese -->
<div class="modal fade" id="modalAnamnese" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-lg" style="width:85%">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_permissoes"></span>				

				</h4>
				<button id="btn-fechar-ana" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			
			<div class="modal-body">
				<div class="row" id="listar_ana">
					
				</div>

				<br>
				<input type="hidden" name="id" id="id_pac_ana">
				<small><div id="mensagem_ana" align="center" class="mt-3"></div></small>		
			</div>

			<div class="modal-footer">       
				<button data-dismiss="modal" type="" class="btn btn-primary">Salvar</button>
			</div>
					
		</div>
	</div>
</div>




<!-- Modal receita -->
<div class="modal fade" id="modalReceita" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-lg" style="width:80%">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_receita"></span>				

				</h4>
				<button id="btn-fechar-receita" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			<form method="POST" action="rel/receita_class.php" target="_blank">
			<div class="modal-body">
				<div class="row">
						<div class="col-md-3">	
								<label>Remédio</label>
								<input type="text" id="remedio" class="form-control" placeholder="Ciprofloxacino 500 mg" >			
							</div>

							<div class="col-md-3">	
								<label>Quantidade</label>
								<input type="text" id="quantidade" class="form-control" placeholder="1 Caixa, 14 Compromidos, etc">			
							</div>	
						
				
					<div class="col-md-5">	
								<label>Forma de Uso</label>
								<input type="text" id="uso" class="form-control" placeholder="1 Comprimido a cada duas horas">			
							</div>	

							<div class="col-md-1" style="margin-top: 22px">
								
								<button onclick="inserirItem()" type="button" class="btn btn-success"><i class="fa fa-check"></i></button>	
							</div>	
				</div>

				<div class="row" style="margin-top: 20px; border-top: 1px solid #595858">
					<div id="listar_remedios">
						
					</div>
				</div>

				<br>
				<input type="hidden" name="id" id="id_receita">
				<small><div id="mensagem_receita" align="center" class="mt-3"></div></small>		
			</div>

			<div class="modal-footer"> 

			<a onclick="limparReceita()" class="btn btn-danger">Limpar Receita</a>

				<button type="submit" class="btn btn-primary">Gerar Receita</button>
			</div>
			</form>		
		</div>
	</div>
</div>






<!-- Modal Atestado -->
<div class="modal fade" id="modalAtestado" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_atestado"></span>				

				</h4>
				<button id="btn-fechar-atestado" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			<form method="POST" action="rel/atestado_class.php" target="_blank">
			<div class="modal-body">
				<div class="row">
						<div class="col-md-6">	
								<label>Data Inicial</label>
								<input type="date" name="dataInicial" class="form-control" placeholder="" value="<?php echo $data_atual ?>">			
							</div>

							<div class="col-md-6">	
								<label>Data Final</label>
								<input type="date" name="dataFinal" class="form-control" placeholder="" value="<?php echo $data_atual ?>" >			
							</div>															
				
						</div>

						<div class="row">
							<div class="col-md-12">	
								<label>Motivo</label>
								<input type="text" name="motivo" class="form-control" placeholder="Motivo do Afastamento" >	
							</div>
						</div>

						<div class="row">
							<div class="col-md-12">	
								<label>Informações Relevantes</label>
								<input type="text" name="obs" class="form-control" placeholder="Demais Informações" >	
							</div>
						</div>

			
				<br>
				<input type="hidden" name="id" id="id_atestado">
				<small><div id="mensagem_atestado" align="center" class="mt-3"></div></small>		
			</div>

			<div class="modal-footer">

				<button type="submit" class="btn btn-primary">Gerar Atestado</button>
			</div>
			</form>		
		</div>
	</div>
</div>






<!-- Modal Exames -->
<div class="modal fade" id="modalExames" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_exame"></span>				

				</h4>
				<button id="btn-fechar-exame" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			<form method="POST" action="rel/exame_class.php" target="_blank">
			<div class="modal-body">
				<div class="row">
						<div class="col-md-5">	
								<label>Exame</label>
								<select class="sel2" id="exame" name="exame" style="width:100%" onchange="trocarExame()">
									<option value="">Outro</option>
								 <?php 
									$query = $pdo->query("SELECT * from procedimentos where exame = 'Sim' order by id asc");
									$res = $query->fetchAll(PDO::FETCH_ASSOC);
									$linhas = @count($res);
									if($linhas > 0){
									for($i=0; $i<$linhas; $i++){
								 ?>
								  <option value="<?php echo $res[$i]['nome'] ?>"><?php echo $res[$i]['nome'] ?></option>

								<?php } } ?>
								</select>				
							</div>

							<div class="col-md-5" style="margin-top: 22px;">	
								
								<input type="text" id="exame2" name="exame2" class="form-control" placeholder="Digite o nome do exame">			
							</div>						
				
				

							<div class="col-md-2" style="margin-top: 22px">
								
								<button onclick="inserirItemExame()" type="button" class="btn btn-success"><i class="fa fa-check"></i></button>	
							</div>	
				</div>

				<div class="row" style="margin-top: 20px; border-top: 1px solid #595858">
					<div id="listar_exames">
						
					</div>
				</div>

				<br>
				<input type="hidden" name="id" id="id_exame">
				<small><div id="mensagem_exame" align="center" class="mt-3"></div></small>		
			</div>

			<div class="modal-footer"> 

			<a onclick="limparExame()" class="btn btn-danger">Limpar Exame</a>

				<button type="submit" class="btn btn-primary">Solicitar Exames</button>
			</div>
			</form>		
		</div>
	</div>
</div>




<script type="text/javascript">var pag = "<?=$pag?>"</script>
<script src="js/ajax.js"></script>

<script type="text/javascript">
	$(document).ready(function() {
    	$('.sel2').select2({
    		dropdownParent: $('#modalExames')
    	});
	});
</script>

<script type="text/javascript">
	function carregarImg() {
		var target = document.getElementById('target');
		var file = document.querySelector("#foto").files[0];


		var arquivo = file['name'];
		resultado = arquivo.split(".", 2);

		if(resultado[1] === 'pdf'){
			$('#target').attr('src', "img/pdf.png");
			return;
		}

		if(resultado[1] === 'rar' || resultado[1] === 'zip'){
			$('#target').attr('src', "img/rar.png");
			return;
		}



		var reader = new FileReader();

		reader.onloadend = function () {
			target.src = reader.result;
		};

		if (file) {
			reader.readAsDataURL(file);

		} else {
			target.src = "";
		}
	}
</script>



<script type="text/javascript">
	function valorData(dataInicio, dataFinal){
	 $('#data-inicial-caixa').val(dataInicio);
	 $('#data-final-caixa').val(dataFinal);	
	listar();
}
</script>



<script type="text/javascript">
	$('#data-inicial-caixa').change(function(){
			//$('#tipo-busca').val('');
			listar();
		});

		$('#data-final-caixa').change(function(){						
			//$('#tipo-busca').val('');
			listar();
		});	
</script>





<script type="text/javascript">
	function listar(){

	var dataInicial = $('#data-inicial-caixa').val();
	var dataFinal = $('#data-final-caixa').val();	
	var status = $('#buscar-contas').val();	


	$('#dataInicial').val(dataInicial);
	$('#dataFinal').val(dataFinal);
	$('#pago_rel').val(status);


	
    $.ajax({
        url: 'paginas/' + pag + "/listar.php",
        method: 'POST',
        data: {dataInicial, dataFinal, status},
        dataType: "html",

        success:function(result){
            $("#listar").html(result);
            $('#mensagem-excluir').text('');
        }
    });
}
</script>



<script type="text/javascript">
	function buscarContas(status){
	 $('#buscar-contas').val(status);
	 listar();
	}
</script>


<script>

	$("#form-historico").submit(function () {
		event.preventDefault();
		var id_pac = $('#id_pac').val();
		var formData = new FormData(this);		

		$.ajax({
			url: 'paginas/' + pag +  "/inserir_historico.php",
			type: 'POST',
			data: formData,

			success: function (mensagem) {
				$('#mensagem-historico').text('');
				$('#mensagem-historico').removeClass()
				if (mensagem.trim() == "Salvo com Sucesso") {    
					listarHistorico(id_pac);
					$('#historico').val('');
				} else {
					$('#mensagem-historico').addClass('text-danger')
					$('#mensagem-historico').text(mensagem)
				}

			},

			cache: false,
			contentType: false,
			processData: false,

		});

	});


	function ficha(){
		var id_pac = $('#id_pac').val();
		window.open("rel/ficha_class.php?id="+id_pac);
	}



	function listarAnamnese(id){
		 $.ajax({
        url: 'paginas/' + pag + "/listar_anamnese.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(result){        	
            $("#listar_ana").html(result);
            $('#mensagem_ana').text('');
        }
    });
	}


	function adicionarItem(id, paciente){
		
		$.ajax({
        url: 'paginas/' + pag + "/add_item.php",
        method: 'POST',
        data: {id, paciente},
        dataType: "html",

        success:function(result){        	
           listarAnamnese(paciente);
        }
    });
	}


	function adicionarDesc(id, paciente){
		var desc = $('#desc_'+id).val();
		$.ajax({
        url: 'paginas/' + pag + "/editar_item.php",
        method: 'POST',
        data: {id, paciente, desc},
        dataType: "html",

        success:function(result){        	
          listarAnamnese(paciente);
        }
    });
	}


	function listarAnaPac(id){
		 $.ajax({
        url: 'paginas/' + pag + "/listar_ana_pac.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(result){        	
            $("#listar_ana_pac").html(result);
           
        }
    });
	}

function inserirItem(){
	var remedio = $("#remedio").val();
	var quantidade = $("#quantidade").val();
	var uso = $("#uso").val();
	var id_paciente = $("#id_receita").val();

	if(remedio == ""){
		alert('Descreva o Remédio!');
		return;
	}

	$('#mensagem_receita').text('');
	 $.ajax({
        url: 'paginas/' + pag + "/inserir_remedio.php",
        method: 'POST',
        data: {id_paciente, remedio, quantidade, uso},
        dataType: "html",

        success:function(result){        	
            if(result.trim() === 'Inserindo com Sucesso'){
            	listarRemedios(id_paciente);
            	limparCamposRemedio()
            }else{
            	$('#mensagem_receita').text(result);
            }
           
        }
    });

}

function listarRemedios(id){
		 $.ajax({
        url: 'paginas/' + pag + "/listar_remedios.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(result){        	
            $("#listar_remedios").html(result);
            $('#mensagem_receita').text('');
        }
    });
	}

function limparCamposRemedio(){
	$("#remedio").val('');
	$("#quantidade").val('');
	$("#uso").val('');
}

function limparReceita(){
	var id_paciente = $("#id_receita").val();
	 $.ajax({
        url: 'paginas/' + pag + "/limpar_receita.php",
        method: 'POST',
        data: {id_paciente},
        dataType: "html",

        success:function(result){        	
            listarRemedios(id_paciente);
            limparCamposRemedio();
        }
    });
}

function trocarExame(){	
	var exame = $("#exame").val();
	
	if(exame == ""){
		$("#exame2").show();
	}else{
		$("#exame2").hide();
	}
	
}



function inserirItemExame(){
	var exame = $("#exame").val();
	var exame2 = $("#exame2").val();	
	var id_paciente = $("#id_exame").val();

	if(exame == "" && exame2 == ""){
		alert('Selecione um Exame ou escreva o nome do exame!');
		return;
	}

	$('#mensagem_exame').text('');
	 $.ajax({
        url: 'paginas/' + pag + "/inserir_exame.php",
        method: 'POST',
        data: {id_paciente, exame, exame2},
        dataType: "html",

        success:function(result){        	
            if(result.trim() === 'Inserindo com Sucesso'){
            	listarExames(id_paciente);
            	limparCamposExame()
            }else{
            	$('#mensagem_receita').text(result);
            }
           
        }
    });

}

function listarExames(id){
		 $.ajax({
        url: 'paginas/' + pag + "/listar_exames.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(result){        	
            $("#listar_exames").html(result);
            $('#mensagem_exame').text('');
        }
    });
	}

function limparCamposExame(){
	$("#exame").val('').change();
	$("#exame2").val('');
	
}

function limparExame(){
	var id_paciente = $("#id_exame").val();
	 $.ajax({
        url: 'paginas/' + pag + "/limpar_exame.php",
        method: 'POST',
        data: {id_paciente},
        dataType: "html",

        success:function(result){        	
            listarExames(id_paciente);
            limparCamposExame();
        }
    });
}
</script>

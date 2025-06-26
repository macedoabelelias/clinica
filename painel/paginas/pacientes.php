<?php 
$pag = 'pacientes';

if(@$pacientes == 'ocultar'){
	echo "<script>window.location='../index.php'</script>";
	exit();
}

?>
<a onclick="inserir()" type="button" class="btn btn-primary"><span class="fa fa-plus"></span> Paciente</a>



<li class="dropdown head-dpdn2" style="display: inline-block;">		
	<a href="#" data-toggle="dropdown"  class="btn btn-danger dropdown-toggle" id="btn-deletar" style="display:none"><span class="fa fa-trash-o"></span> Deletar</a>

	<ul class="dropdown-menu">
		<li>
			<div class="notification_desc2">
				<p>Excluir Selecionados? <a href="#" onclick="deletarSel()"><span class="text-danger">Sim</span></a></p>
			</div>
		</li>										
	</ul>
</li>

<div class="bs-example widget-shadow" style="padding:15px" id="listar">

</div>


<input type="hidden" id="ids">

<!-- Modal Perfil -->
<div class="modal fade" id="modalForm" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-lg">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="titulo_inserir"></span></h4>
				<button id="btn-fechar" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			<form id="form">
				<div class="modal-body">


					<div class="row">
						<div class="col-md-3">							
							<label>Nome</label>
							<input type="text" class="form-control" id="nome" name="nome" placeholder="Seu Nome" required>							
						</div>


						<div class="col-md-3">							
							<label>CPF</label>
							<input type="text" class="form-control" id="cpf" name="cpf" placeholder="CPF" required>							
						</div>

						<div class="col-md-3">							
							<label>Telefone</label>
							<input type="text" class="form-control" id="telefone" name="telefone" placeholder="Seu Telefone" required>							
						</div>


						<div class="col-md-3">							
							<label>Data Nascimento</label>
							<input type="date" class="form-control" id="data_nasc" name="data_nasc" required>							
						</div>

						
					</div>


					<div class="row">	
								
										
							<div class="col-md-5">	
									<label>Profissão</label>
									<input type="text" class="form-control" name="profissao" id="profissao">
								</div>

						


							<div class="col-md-2">	
								<label>Sexo</label>
								<select class="form-control" name="sexo" id="sexo">
									<option value="M">M</option>
									<option value="F">F</option>
									
								</select>						
							</div>

							

							<div class="col-md-2">	
								<label>Tipo Sanguíneo</label>
								<select class="form-control" name="tipo_sanguineo" id="tipo_sanguineo">
									<option value="O">O</option>
									<option value="A">A</option>
									<option value="B">B</option>
									<option value="AB">AB</option>
								</select>						
							</div>


							<div class="col-md-3">	
								<label>Convênio</label>
								<select class="form-control" name="convenio" id="convenio">
									<option value="0">Nenhum</option>
									<?php 
									$query = $pdo->query("SELECT * from convenios order by id asc");
									$res = $query->fetchAll(PDO::FETCH_ASSOC);
									$linhas = @count($res);
									if($linhas > 0){
										for($i=0; $i<$linhas; $i++){
											?>
											<option value="<?php echo $res[$i]['id'] ?>"><?php echo $res[$i]['nome'] ?></option>

										<?php } } ?>
									</select>	

								</div>						
							</div>

							<div class="row">

									<div class="col-md-8">	


								<label>Endereço</label>
								<input type="text" class="form-control" id="endereco" name="endereco" placeholder="Seu Endereço" >							
							</div>	

							<div class="col-md-4">	
								<label>Estado Cívil</label>
								<select class="form-control" name="estado_civil" id="estado_civil">
									<option value="Solteiro">Solteiro(a)</option>
									<option value="Casado">Casado(a)</option>
									<option value="Víuvo">Víuvo(a)</option>
									<option value="Divorciado">Divorciado(a)</option>
								</select>						
							</div>	

							
								
							</div>


							<div class="row">
								<div class="col-md-12">	
									<label>Observações</label>
									<input type="text" class="form-control" name="obs" id="obs">
								</div>
							</div>

							<hr>

							<div class="row">
						<div class="col-md-5">							
							<label>Nome Responsável</label>
							<input type="text" class="form-control" id="nome_responsavel" name="nome_responsavel" placeholder="Seu Nome">							
						</div>


						<div class="col-md-3">							
							<label>CPF Responsável</label>
							<input type="text" class="form-control" id="cpf_responsavel" name="cpf_responsavel" placeholder="CPF Responsável">							
						</div>					
						
					</div>


				
						<input type="hidden" class="form-control" id="id" name="id">					

						<br>
						<small><div id="mensagem" align="center"></div></small>
					</div>
					<div class="modal-footer">       
						<button type="submit" class="btn btn-primary">Salvar</button>
					</div>
				</form>
			</div>
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
						<span style="margin-right: 20px"><b>CPF</b> <span id="cpf_dados"></span></span>

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
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_anamnese"></span>				

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








	<!-- Modal Arquivos -->
	<div class="modal fade" id="modalArquivos" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h4 class="modal-title" id="tituloModal">Gestão de Arquivos - <span id="nome-arquivo"> </span></h4>
					<button id="btn-fechar-arquivos" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -20px">
						<span aria-hidden="true">&times;</span>
					</button>
				</div>
				<form id="form-arquivos" method="post">
					<div class="modal-body">

						<div class="row">
							<div class="col-md-8">						
								<div class="form-group"> 
									<label>Arquivo</label> 
									<input class="form-control" type="file" name="arquivo_conta" onChange="carregarImgArquivos();" id="arquivo_conta">
								</div>	
							</div>
							<div class="col-md-4" style="margin-top:-10px">	
								<div id="divImgArquivos">
									<img src="images/arquivos/sem-foto.png"  width="60px" id="target-arquivos">									
								</div>					
							</div>




						</div>

						<div class="row" style="margin-top:-40px">
							<div class="col-md-8">
								<input type="text" class="form-control" name="nome-arq"  id="nome-arq" placeholder="Nome do Arquivo * " required>
							</div>

							<div class="col-md-4">										 
								<button type="submit" class="btn btn-primary">Inserir</button>
							</div>
						</div>

						<hr>

						<small><div id="listar-arquivos"></div></small>

						<br>
						<small><div align="center" id="mensagem-arquivo"></div></small>

						<input type="hidden" class="form-control" name="id-arquivo"  id="id-arquivo">


					</div>
				</form>
			</div>
		</div>
</div>



<!-- Modal ficha -->
<div class="modal fade" id="modalFicha" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_ficha"></span>				

				</h4>
				<button id="btn-fechar-ficha" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			<form method="POST" action="rel/ficha_class.php" target="_blank">
			<div class="modal-body">
				<div class="row">
						<div class="col-md-6">	
								<label>Mostrar Histórico</label>
								<select class="form-control" name="historico">
									<option value="1000">Tudo</option>
									<option value="5">5 Últimos</option>
									<option value="10">10 Últimos</option>
									<option value="20">20 Últimos</option>
									<option value="Não">Nenhum</option>
								</select>						
							</div>	


							<div class="col-md-6">	
								<label>Mostrar Anamnese</label>
								<select class="form-control" name="anamnese">
									<option value="">Mostrar em duas Colunas</option>
									<option value="1">Mostrar em uma Coluna</option>
									<option value="Não">Não Mostrar</option>
								</select>						
							</div>	
				</div>

				<br>
				<input type="hidden" name="id" id="id_ficha">
				<small><div id="mensagem_ficha" align="center" class="mt-3"></div></small>		
			</div>

			<div class="modal-footer">       
				<button type="submit" class="btn btn-primary">Gerar Ficha</button>
			</div>
			</form>		
		</div>
	</div>
</div>




<!-- Modal consultas -->
<div class="modal fade" id="modalConsultas" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-lg">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_consulta"></span>				

				</h4>
				<button id="btn-fechar-consulta" type="button" class="close" data-dismiss="modal" aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			
			<div class="modal-body">
				<div id="listar_consultas"></div>
			</div>

			
		</div>
	</div>
</div>



	<script type="text/javascript">var pag = "<?=$pag?>"</script>
	<script src="js/ajax.js"></script>



<script type="text/javascript">
			function carregarImgArquivos() {
				var target = document.getElementById('target-arquivos');
				var file = document.querySelector("#arquivo_conta").files[0];

				var arquivo = file['name'];
				resultado = arquivo.split(".", 2);

				if(resultado[1] === 'pdf'){
					$('#target-arquivos').attr('src', "images/pdf.png");
					return;
				}

				if(resultado[1] === 'rar' || resultado[1] === 'zip'){
					$('#target-arquivos').attr('src', "images/rar.png");
					return;
				}

				if(resultado[1] === 'doc' || resultado[1] === 'docx' || resultado[1] === 'txt'){
					$('#target-arquivos').attr('src', "images/word.png");
					return;
				}


				if(resultado[1] === 'xlsx' || resultado[1] === 'xlsm' || resultado[1] === 'xls'){
					$('#target-arquivos').attr('src', "images/excel.png");
					return;
				}


				if(resultado[1] === 'xml'){
					$('#target-arquivos').attr('src', "images/xml.png");
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
			$("#form-arquivos").submit(function () {
				event.preventDefault();
				var formData = new FormData(this);

				$.ajax({
					url: 'paginas/' + pag + "/arquivos.php",
					type: 'POST',
					data: formData,

					success: function (mensagem) {
						$('#mensagem-arquivo').text('');
						$('#mensagem-arquivo').removeClass()
						if (mensagem.trim() == "Inserido com Sucesso") {                    
						//$('#btn-fechar-arquivos').click();
						$('#nome-arq').val('');
						$('#arquivo_conta').val('');
						$('#target-arquivos').attr('src','images/arquivos/sem-foto.png');
						listarArquivos();
					} else {
						$('#mensagem-arquivo').addClass('text-danger')
						$('#mensagem-arquivo').text(mensagem)
					}

				},

				cache: false,
				contentType: false,
				processData: false,

			});

			});
		</script>

		<script type="text/javascript">
			function listarArquivos(){
				var id = $('#id-arquivo').val();	
				$.ajax({
					url: 'paginas/' + pag + "/listar-arquivos.php",
					method: 'POST',
					data: {id},
					dataType: "text",

					success:function(result){
						$("#listar-arquivos").html(result);
					}
				});
			}

		</script>



<script>

	$("#form-historico").submit(function () {
		pag = 'consultas';
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
		pag = 'consultas';
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
		pag = 'consultas';
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
		pag = 'consultas';
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
		pag = 'consultas';
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


</script>

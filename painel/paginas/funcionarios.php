<?php
$pag ='funcionarios';

if(@$funcionarios == 'ocultar'){
	echo "<script>window.location='../index.php'</script>";
	exit();
}

 ?>

<a onclick="inserir()" type="button" class="btn btn-primary"><span class="fa fa-plus"></span> Funcionario</a>

<li class="dropdown head-dpdn2" style="display: inline-block;">
	<a href="#" data-toggle="dropdown" class="btn btn-danger dropdown-toggle" id="btn-deletar"
	style="display:none"><span class="fa fa-trash-o"></span> Excluir</a>
           
        <ul class="dropdown-menu">
            <li>
            <div class="notification_desc2">
            <p>Excluir os Selecionados? <a href="#" onclick="excluirSel()"><span class
               ="text-danger">Sim</span></a></p>
            </div>
            </li>										
        </ul>           
</li>


<div class="bs-example widget-shadow" style="padding:15px" id="listar"></div>
</div>
<input type="hidden" id="ids">

<!-- Modal Perfil -->
<div class="modal fade" id="modalForm" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog">
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
						<div class="col-md-6">							
								<label>Nome</label>
								<input type="text" class="form-control" id="nome" name="nome" 
                                placeholder="Seu Nome" required>							
						</div>

						<div class="col-md-6">							
								<label>Email</label>
								<input type="email" class="form-control" id="email" name="email" 
                                placeholder="Seu E-mail" required>							
						</div>
					</div>


					<div class="row">
						<div class="col-md-12">							
								<label>Endereço</label>
								<input type="text" class="form-control" id="endereco" name="endereco" 
                                placeholder="Endereço completo">							
						</div>
                    </div>

                    <div class="row">

					<div class="col-md-4">							
								<label>CPF</label>
								<input type="text" class="form-control" id="cpf" name="cpf" 
                                placeholder="CPF" required>							
						</div>

						<div class="col-md-4">							
								<label>Telefone</label>
								<input type="text" class="form-control" id="telefone" name="telefone" 
                                placeholder="Seu Telefone" required>							
						</div>
                        
                        <div class="col-md-4">							
								<label>Nível</label>
								<select class="form-control" name="nivel" id="nivel" required>
								<?php 
									$query = $pdo->query("SELECT * from cargos order by id asc");
									$res = $query->fetchAll(PDO::FETCH_ASSOC);
									$linhas = @count($res);
									if($linhas > 0){
									for($i=0; $i<$linhas; $i++){
									?>
									<option value="<?php echo $res[$i]['nome'] ?>">
										<?php  echo $res[$i]['nome']?></option>
									

									<?php }}else{ ?>
										<option value="">Cadastre um Cargo</option>
									<?php }?>
                                </select>
						</div>						
					</div>

					<div class="row">
						<div class="col-md-3">							
								<label>Atendimento</label>
								<select class="form-control" name="atendimento" id="atendimento">
									<option value="Não">Não</option>
									<option value="Sim">Sim</option>
								</select>
						</div>

						<div class="col-md-3">							
								<label>Comissão %</label>
								<input type="number" class="form-control" id="comissao" name="comissao" 
                                placeholder="Porcentagem Comissão">							
						</div>

						<div class="col-md-6">							
								<label>Dados Pagamento</label>
								<input type="text" class="form-control" id="pagamento" name="pagamento" 
                                placeholder="Chave PIX">							
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

<!-- Modal Dados -->
<div class="modal fade" id="modalDados" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="titulo_dados"></span></h4>
				<button id="btn-fechar-dados" type="button" class="close" data-dismiss="modal" 
					aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			
			<div class="modal-body">
			<div class="row" style="margin-top: 0px">
					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>Telefone: </b></span><span id="telefone_dados"></span>
					</div>

					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>Email: </b></span><span id="email_dados"></span>
					</div>	
					
					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>CPF: </b></span><span id="cpf_dados"></span>
					</div>	

					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>Nível: </b></span><span id="nivel_dados"></span>
					</div>

					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>Ativo: </b></span><span id="ativo_dados"></span>
					</div>

					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>Data Cadastro: </b></span><span id="data_dados"></span>
					</div>

					<div class="col-md-12" style="margin-bottom: 5px">
						<span><b>Endereço: </b></span><span id="endereco_dados"></span>
					</div>

					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>Atendimento: </b></span><span id="atendimento_dados"></span>
					</div>

					<div class="col-md-6" style="margin-bottom: 5px">
						<span><b>Comissão: </b></span><span id="comissao_dados"></span>
					</div>

					<div class="col-md-12" style="margin-bottom: 5px">
						<span><b>Dados Pagamento: </b></span><span id="pagamento_dados"></span>
					</div>

					<div class="col-md-12" style="margin-bottom: 5px">
						<div align="center"><img src="" id="foto_dados" width="200px"></div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>


<!-- Modal Procedimentos -->
<div class="modal fade" id="modalProcedimentos" tabindex="-1" aria-labelledby="exampleModalLabel" 
aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<h4 class="modal-title" id="exampleModalLabel"><span id="nome_procedimento"></span></h4>

				<button id="btn-fechar-procedimentos" type="button" class="close" data-dismiss="modal" 
				aria-label="Close" style="margin-top: -25px">
					<span aria-hidden="true">&times;</span>
				</button>
			</div>
			
			<form id="form_procedimento">
			<div class="modal-body">
				<div class="row">
					<div class="col-md-8">
					<select class="sel" name="procedimento" id="procedimento" required style="width:100%">
								<?php 
									$query = $pdo->query("SELECT * from procedimentos order by id asc");
									$res = $query->fetchAll(PDO::FETCH_ASSOC);
									$linhas = @count($res);
									if($linhas > 0){
									for($i=0; $i<$linhas; $i++){
									?>
									<option value="<?php echo $res[$i]['id'] ?>">
										<?php  echo $res[$i]['nome']?></option>
									

									<?php }}else{ ?>
										<option value="">Cadastre um Procedimento</option>
									<?php }?>
                                </select>
					</div>

					<div class="col-md-4">
						<button id="btn_procedimento" type="submit" class="btn btn-primary">Inserir</button>
					</div>
				</div>
				<div class="row" id="listar_procedimentos">
					
				</div>
				<br>
				<input type="hidden" name="id" id="id_procedimento">
				<small><div id="mensagem_procedimento" align="center" class="mt-3"></div></small>		
			</div>
		</form>
					
		</div>
	</div>
</div>




<script type="text/javascript">var pag = "<?=$pag?>"</script>
<script src="js/ajax.js"></script>

<script type="text/javascript">
$(document).ready(function() {
    $('.sel').select2({
		dropdownParent:$('#modalProcedimentos')
	});
});
</script>

<script type="text/javascript">

$("#form_procedimento").submit(function () {

	var usuario = $('#id_procedimento').val();

event.preventDefault();
var formData = new FormData(this);

$.ajax({
	url: 'paginas/' + pag + "/inserir_procedimento.php",
	type: 'POST',
	data: formData,

	success: function (mensagem) {
		$('#mensagem_procedimento').text('');
		$('#mensagem_procedimento').removeClass()
		if (mensagem.trim() == "Salvo com Sucesso") {

			//$('#btn-fechar-procedimentos').click();
			listarProcedimentos(usuario);          

		} else {

			$('#mensagem_procedimento').addClass('text-danger')
			$('#mensagem_procedimento').text(mensagem)
		}


	},

	cache: false,
	contentType: false,
	processData: false,

});

});

function listarProcedimentos(id){
	$.ajax({
        url: 'paginas/' + pag + "/listar_procedimentos.php",
        method: 'POST',
        data: {id},
        dataType: "html",

        success:function(result){
            $("#listar_procedimentos").html(result);            
        }
    });
}
</script>







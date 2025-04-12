<?php
$pag ='convenios';

if(@$convenios == 'ocultar'){
	echo "<script>window.location='../index.php'</script>";
	exit();
}
 ?>
<div class="main-page margin-mobile">
<a onclick="inserir()" type="button" class="btn btn-primary"><span class="fa fa-plus">	
</span> Convênio</a>



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
                                placeholder="Nome do Convênio" required>							
						</div>

						<div class="col-md-3">							
								<label>Comissão%</label>
								<input type="number" class="form-control" id="comissao" name="comissao" 
                                placeholder="Se houver">							
						</div>

						<div class="col-md-3" style="margin-top: 22px">							
						<button type="submit" class="btn btn-primary">Salvar</button>						
						</div>
					</div>
					

					<input type="hidden" class="form-control" id="id" name="id">				

				<br>
				<small><div id="mensagem" align="center"></div></small>
			</div>
			
			</form>
		</div>
	</div>
</div>



<script type="text/javascript">var pag = "<?=$pag?>"</script>
<script src="js/ajax.js"></script>

<script type="text/javascript">
	function carregarImg() {
    var target = document.getElementById('target');
    var file = document.querySelector("#foto").files[0];
    
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



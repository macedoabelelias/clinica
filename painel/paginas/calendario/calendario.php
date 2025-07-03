<script>
	function modalShow() {		
		$('#modalShow').modal('show');
	}

	$(document).ready(function() {
		$('#calendar').fullCalendar({


		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay,listYear'
		},

		defaultDate:'<?php echo date('Y-m-d'); ?>',
		editable: true,
		navLinks: true,
		eventLimit: true,
		selectable: true,
		selectHelper: true,
		select: function(start, end) {
			
			var inicio = start.format('YYYY-MM-DD');
			$('#ModalAdd #data-modal').val(inicio);
			listarHorarios()
			$('#ModalAdd #botao_excluir').hide();
			$('#ModalAdd #botao_confirmar').hide();
			$('#ModalAdd').modal('show');
		},
		eventRender: function(event, element) {
			
			
			element.bind('click', function() {
				$('#ModalAdd #botao_excluir').show();
				$('#ModalAdd #botao_confirmar').show();
				$('#ModalAdd #myModalLabel').text('Editar Agendamento');
				$('#ModalAdd #id').val(event.id);
				$('#ModalAdd #cliente').val(event.cliente).change();
				$('#ModalAdd #funcionario_modal').val(event.profissional).change();

				setTimeout(function(){
					$('#ModalAdd #servico').val(event.servico).change();
				}, 500); 	

				$('#ModalAdd #data-modal').val(event.start.format('YYYY-MM-DD'));
				$('#ModalAdd #obs').val(event.description);
				$('#ModalAdd #retorno').val(event.retorno).change();
				//$('#ModalAdd #hora').val(event.hora);
				//$('#ModalEdit #inicio').val(event.start.format('DD-MM-YYYY HH:mm:ss'));
				//$('#ModalEdit #termino').val(event.end.format('DD-MM-YYYY HH:mm:ss'));

				listarHorarios();
				$('#ModalAdd').modal('show');
			});
		},
		eventDrop: function(event, delta, revertFunc) { 

			edit(event);
		},
					
		eventResize: function(event,dayDelta,minuteDelta,revertFunc) { 

			edit(event);
		},

		events: [
					<?php for($i_ini=0; $i_ini < $total_reg_ini; $i_ini++){
						$data_inicio = $res_ini[$i_ini]['data']." ".$res_ini[$i_ini]['hora'];
						$data_final = $res_ini[$i_ini]['data']." ".$res_ini[$i_ini]['hora'];

						$hora_inicio = $res_ini[$i_ini]['hora'];
						$hora_final = $res_ini[$i_ini]['hora'];
						
						if($hora_inicio == '00:00:00' || $hora_inicio == ''){
							$start = $res_ini[$i_ini]['data'];
						}else{
							$start = $data_inicio;
						}
						if($hora_final == '00:00:00' || $hora_inicio == ''){
							$end = $res_ini[$i_ini]['data'];
						}else{
							$end = $data_final;
						}

						
						$paciente = $res_ini[$i_ini]['paciente'];
						$query2 = $pdo->query("SELECT * FROM pacientes where id = '$paciente'");
						$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
						if(@count($res2) > 0){
							$nome_cliente = $res2[0]['nome'];							
						}else{
							$nome_cliente = 'Sem Cliente';
							
						}


						$funcionario = $res_ini[$i_ini]['funcionario'];
						$query2 = $pdo->query("SELECT * FROM usuarios where id = '$funcionario'");
						$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
						if(@count($res2) > 0){
							$profissional = $res2[0]['nome'];							
						}else{
							$profissional = 'Sem Registro';
							
						}

						$servico = $res_ini[$i_ini]['servico'];
						$query2 = $pdo->query("SELECT * FROM procedimentos where id = '$servico'");
						$res2 = $query2->fetchAll(PDO::FETCH_ASSOC);
						if(@count($res2) > 0){
							$nome_servico = $res2[0]['nome'];							
						}else{
							$nome_servico = 'Sem Serviço';
							
						}

						if($res_ini[$i_ini]['status'] == "Agendado"){
							$cor_agd = "#80050b";
						}else{
							$cor_agd = "#011436";
						}


					?>
					{
						id: '<?php echo $res_ini[$i_ini]['id'] ?>',
						title: '<?php echo $nome_servico ?> / Paciente <?php echo $nome_cliente ?> / Médico: <?php echo $profissional ?>',
						description: '<?php echo $res_ini[$i_ini]['obs'] ?>',
						start: '<?php echo $start; ?>',
						end: '<?php echo $end; ?>',
						color: '<?php echo $cor_agd ?>',
						cliente: '<?php echo $res_ini[$i_ini]['paciente'] ?>',
						servico: '<?php echo $res_ini[$i_ini]['servico'] ?>',
						status:'<?php echo $res_ini[$i_ini]['status'] ?>',
						profissional:'<?php echo $funcionario ?>',
						retorno:'<?php echo $res_ini[$i_ini]['retorno'] ?>',
						hora:'<?php echo $res_ini[$i_ini]['hora'] ?>',
					},
					<?php } ?>
				]
			});
				
				function edit(event){
					var id = event.id;
					var cliente = event.cliente;
					var funcionario = event.profissional;
					var servico = event.servico;
					var data = event.start.format('YYYY-MM-DD');
					var obs = event.description;
					var retorno = event.retorno;
					var hora = event.hora;

					 $.ajax({
				        url: 'paginas/' + pag + "/inserir.php",
				        method: 'POST',
				        data: {id, cliente, funcionario, servico, data, obs, retorno, hora},
				        dataType: "html",

				        success:function(mensagem){
				             //alert(mensagem)
				            if (mensagem.trim() == "Salvo com Sucesso") { 
				            	
				            } else {
				               alert(mensagem);

				            }

				            chamarCalendario();
				        }
				    });

				}
		});

</script>



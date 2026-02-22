package mercadona_prueba.controller;

import mercadona_prueba.dto.ReporteEstadoDTO;
import mercadona_prueba.dto.ReporteFaltasDTO;
import mercadona_prueba.service.ReporteService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/reportes")
public class ReporteController 
{
    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    private final ReporteService reporteService;
    
    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
   
    public ReporteController(ReporteService reporteService) { this.reporteService = reporteService; }

    // -- -------------------- --
    // -- TODO ENDPOINT ESTADO --
    // -- -------------------- --

    @GetMapping("/tiendas/{codigoTienda}/estado")
    public ResponseEntity<ReporteEstadoDTO> obtenerReporteEstado(@PathVariable Integer codigoTienda) 
    {
        ReporteEstadoDTO reporte = reporteService.generarReporteEstado(codigoTienda);
        return ResponseEntity.ok(reporte);
    }

    // -- -------------------- --
    // -- TODO ENDPOINT FALTAS --
    // -- -------------------- --

    @GetMapping("/tiendas/{codigoTienda}/faltas")
    public ResponseEntity<ReporteFaltasDTO> obtenerReporteFaltas_MemoriaJava(@PathVariable Integer codigoTienda) 
    {
        ReporteFaltasDTO reporte = reporteService.generarReporteFaltas(codigoTienda,false);
        return ResponseEntity.ok(reporte);
    }
    
    @GetMapping("/tiendas/{codigoTienda}/faltasJPQL")
    public ResponseEntity<ReporteFaltasDTO> obtenerReporteFaltas_JPQL(@PathVariable Integer codigoTienda) 
    {
        ReporteFaltasDTO reporte = reporteService.generarReporteFaltas(codigoTienda,true);
        return ResponseEntity.ok(reporte);
    }
}
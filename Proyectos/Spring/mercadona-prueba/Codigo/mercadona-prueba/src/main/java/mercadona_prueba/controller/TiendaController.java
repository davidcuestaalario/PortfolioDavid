package mercadona_prueba.controller;

import mercadona_prueba.dto.AptitudesForTienda;
import mercadona_prueba.service.TiendaService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/tiendas")
public class TiendaController 
{
    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    private final TiendaService tiendaService;

    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
   
    public TiendaController(TiendaService tiendaService) { this.tiendaService = tiendaService; }

    // -- -------------------- --
    // -- TODO ENDPOINT ESTADO --
    // -- -------------------- --

    @GetMapping("/{codigoTienda}")
    public ResponseEntity<AptitudesForTienda> obtenerTienda(@PathVariable Integer codigoTienda) 
    {
        AptitudesForTienda respuesta = tiendaService.obtenerDetalleTienda(codigoTienda);
        return ResponseEntity.ok(respuesta);
    }
}
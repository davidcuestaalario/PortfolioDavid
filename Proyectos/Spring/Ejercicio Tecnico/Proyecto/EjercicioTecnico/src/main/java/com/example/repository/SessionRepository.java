package com.example.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.model.Session;

import java.util.List;

public interface SessionRepository extends JpaRepository<Session, Long> 
{

    /** 
     * Permite listar todas las sessiones con un estado de actividad
     * @param active = Sesiones activas (TRUE) o inactivas (FALSE)
     * @return Listado de sessiones 
     */
    List<Session> findByActive(Boolean active);
    
    /** 
     * Permite listar todas las sesiones de un usuario con un estado de actividad
     * @param userId = Identificador del usuario
     * @param active = Sesiones activas (TRUE) o inactivas (FALSE) 
     * @return Listado de sessiones
     */
    List<Session> findByUserIdAndActive( Long userId , Boolean active );
    
    /** 
     * Permite identificar si una session es valida
     * @param token = ID de la session
     * @param active = Sesiones activas (TRUE) o inactivas (FALSE)
     * @return
     */
    Session findByTokenAndActive(String token, Boolean active);
}
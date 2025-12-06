package com.example.service;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import com.example.dto.UserRequestDTO;
import com.example.dto.UserResponseDTO;
import com.example.mapper.UserMapper;
import com.example.model.User;
import com.example.repository.UserRepository;

import java.util.Optional;

// Pruebas unitarias para el servicio del usuario
// La anotacion @ExtendWith le dice a JUnit que use Mockito para procesar las anotaciones @Mock
// La anotacion @Mock crea un objeto falso. No conecta con base de datos, ni hace nada real
// Solo la simula establecer la conexion a efectos de las pruebas y se inventa un resultado
// Esto es asi para poder probar este modulo especifico sin que intervengan los demas
// De modo que si surge algun error no puede haber sido en otro modulo (porque los demas modulos estan "fingidos")
// La anotacion @InjectMocks si crea un objeto real e inyecta dentro las dependencias que sean necesarias
@ExtendWith(MockitoExtension.class) 
public class UserServiceTest 
{
	// --------------- DEPENDENCIAS --------------- //
	
	// Instancias falsas
    @Mock private UserRepository userRepository;
    @Mock private UserMapper userMapper;
    
    // Instancias reales
    @InjectMocks private UserService userService;

	// ------------------ PRUEBAS ----------------- //
    
    // Verificar que createUser funciona bien cuando todo es correcto
    @Test
    void testCreateUser_Success() 
    {
    	// ----------- CONFIGURACION ----------- //

        // Datos de entrada ficticios
        UserRequestDTO requestDTO = new UserRequestDTO("nuevoUser", "pass123", "USER", false);
        // Entidad ficticia que devolvería el mapper
        User userEntity = new User();
        userEntity.setUsername("nuevoUser");
        userEntity.setPassword("pass123");
        // Entidad ficticia que devolvería la base de datos
        User savedUserEntity = new User();
        savedUserEntity.setId(1L);
        savedUserEntity.setUsername("nuevoUser");
        // DTO final esperado
        UserResponseDTO expectedResponse = new UserResponseDTO();
        expectedResponse.setId(1L);
        expectedResponse.setUsername("nuevoUser");
        
    	// ----------- ENTRENAMIENTO ----------- //
        
        // "Cuando el mapper convierta el DTO, devuelve mi entidad userEntity"
        Mockito.when(userMapper.toEntity(requestDTO)).thenReturn(userEntity);
        // "Cuando el repositorio guarde CUALQUIER usuario, devuelve mi savedUserEntity"
        Mockito.when(userRepository.save(Mockito.any(User.class))).thenReturn(savedUserEntity);
        // "Cuando el mapper convierta la entidad guardada a DTO, devuelve expectedResponse"
        Mockito.when(userMapper.toDto(savedUserEntity)).thenReturn(expectedResponse);

        // ------------- EJECUCION ------------- //

        // Llamamos al método real del servicio
        UserResponseDTO result = userService.createUser(requestDTO);

        // ------------ VERIFICACION ----------- //
        
        // Comprobamos que el resultado no sea nulo y tenga el ID 1
        Assertions.assertNotNull(result);
        Assertions.assertEquals(1L, result.getId());
        Assertions.assertEquals("nuevoUser", result.getUsername());
        // Comprobamos que el servicio llamó al repositorio exactamente 1 vez
        Mockito.verify(userRepository, Mockito.times(1)).save(userEntity);
    }

    // Verificar búsqueda por ID
    @Test
    void testFindUserById_Found() 
    {
    	// ----------- CONFIGURACION ----------- //
    	// Entidad ficticia que devolvería la base de datos
        Long userId = 1L;
        User foundUser = new User();
        foundUser.setId(userId);
        // DTO final esperado
        UserResponseDTO responseDTO = new UserResponseDTO();
        responseDTO.setId(userId);
        
        // ----------- ENTRENAMIENTO ----------- //
        
        Mockito.when(userRepository.findById(userId)).thenReturn(Optional.of(foundUser));
        Mockito.when(userMapper.toDto(foundUser)).thenReturn(responseDTO);

        // ------------- EJECUCION ------------- //
        
        Optional<UserResponseDTO> result = userService.findUserById(userId);

        // ------------ VERIFICACION ----------- //
        // Comprobamos que el resultado no sea nulo
        Assertions.assertTrue(result.isPresent());
        // Comprobamos que el resultado sea el que esperabamos
        Assertions.assertEquals(userId, result.get().getId());
    }
}
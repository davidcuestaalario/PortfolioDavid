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
    
    // Buscar un ID que no existe
    @Test
    void testFindUserById_NotFound() 
    {
    	// Inventamos un Id que no exista
        Long nonExistentId = 99L;
        // Simulamos que el repositorio devuelve una caja vacía
        Mockito.when(userRepository.findById(nonExistentId)).thenReturn(Optional.empty());
        Optional<UserResponseDTO> result = userService.findUserById(nonExistentId);
        Assertions.assertTrue(result.isEmpty()); // Debe estar vacío
        // Verificamos que NO se llamó al mapper (porque no había nada que mapear)
        Mockito.verify(userMapper, Mockito.never()).toDto(Mockito.any(User.class));
    }
    
    
    // Actualizar usuario existente
    @Test
    void testUpdateUser_Success() 
    {
        // Cogemos el primer id
        Long userId = 1L;
        // Datos nuevos que llegan
        UserRequestDTO updateInfo = new UserRequestDTO();
        updateInfo.setUsername("nombreCambiado");
        updateInfo.setRole("ADMIN");
        // Usuario que ya existe en BD
        User existingUser = new User();
        existingUser.setId(userId);
        existingUser.setUsername("usuario1");
        existingUser.setRole("USER");
        // Usuario simulado después de guardar
        User savedUser = new User();
        savedUser.setId(userId);
        savedUser.setUsername("nombreCambiado"); // Ya actualizado
        // Respuesta esperada
        UserResponseDTO expectedResponse = new UserResponseDTO();
        expectedResponse.setId(userId);
        expectedResponse.setUsername("nombreCambiado");
        // ENTRENAMIENTO
        Mockito.when(userRepository.findById(userId)).thenReturn(Optional.of(existingUser));
        Mockito.when(userRepository.save(Mockito.any(User.class))).thenReturn(savedUser);
        Mockito.when(userMapper.toDto(savedUser)).thenReturn(expectedResponse);
        // VERIFICACION
        Optional<UserResponseDTO> result = userService.updateUser(userId, updateInfo);
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals("nombreCambiado", result.get().getUsername()); 
        // Verificamos que se llamó a guardar
        Mockito.verify(userRepository).save(existingUser);
    }

    // Intentar actualizar un usuario que no existe
    @Test
    void testUpdateUser_NotFound() 
    {
    	// Inventamos un Id que no exista
        Long userId = 99L;
        UserRequestDTO updateInfo = new UserRequestDTO();
        // ENTRENAMIENTO
        Mockito.when(userRepository.findById(userId)).thenReturn(Optional.empty());
        // VERIFICACION
        Optional<UserResponseDTO> result = userService.updateUser(userId, updateInfo);
        Assertions.assertTrue(result.isEmpty());
        // Aseguramos que NUNCA se intentó guardar nada en BD
        Mockito.verify(userRepository, Mockito.never()).save(Mockito.any());
    }    
    
    
    // Bloquear usuario existente
    @Test
    void testBlockUser_Success() 
    {
        // CONFIGURACION
        Long userId = 1L;
        User existingUser = new User();
        existingUser.setId(userId);
        existingUser.setBlocked(false); 
        // ENTRENAMIENTO
        Mockito.when(userRepository.findById(userId)).thenReturn(Optional.of(existingUser));
        Mockito.when(userRepository.save(Mockito.any(User.class))).thenReturn(existingUser);
        // Simulamos la respuesta
        UserResponseDTO responseDTO = new UserResponseDTO();
        responseDTO.setBlocked(true);
        Mockito.when(userMapper.toDto(existingUser)).thenReturn(responseDTO);
        // VERIFICACION
        Optional<UserResponseDTO> result = userService.blockUser(userId);
        Assertions.assertTrue(result.isPresent());
        Assertions.assertTrue(result.get().getBlocked());
        // Verificamos que el objeto se modificó a true antes de guardar
        Assertions.assertTrue(existingUser.getBlocked()); 
    }
    
    // Filtrar solo por ROL
    @Test
    void testFindAllUsers_FilterByRole()
    {
        // CONFIGURACION
        String role = "ADMIN";
        String username = null; // Sin nombre
        // VERIFICACION
        userService.findAllUsers(role, username);
        // Verificamos que llamó al método específico del repositorio
        Mockito.verify(userRepository).findByRole(role);
        // Y aseguramos que NO llamó a los otros
        Mockito.verify(userRepository, Mockito.never()).findAll();
    }

    // Filtrar solo por USERNAME
    @Test
    void testFindAllUsers_FilterByUsername() 
    {
        // CONFIGURACION
        String role = null;
        String username = "pepe";
        // VERIFICACION
        userService.findAllUsers(role, username);
        Mockito.verify(userRepository).findByUsernameContainingIgnoreCase(username);
    }

    // Filtrar por AMBOS
    @Test
    void testFindAllUsers_FilterByBoth() 
    {
        // CONFIGURACION
        String role = "ADMIN";
        String username = "pepe";
        // VERIFICACIONN
        userService.findAllUsers(role, username);
        Mockito.verify(userRepository).findByRoleAndUsernameContainingIgnoreCase(role, username);
    }

    // Sin filtros (Devolver todos)
    @Test
    void testFindAllUsers_NoFilters() 
    {
        // CONFIGURACION
        String role = null;
        String username = null;
        // VERIFICACION
        userService.findAllUsers(role, username);
        Mockito.verify(userRepository).findAll();
    }
}
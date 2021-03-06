set client_encoding='LATIN1';
set search_path='udm';

delete from t_udm_ciudad;
delete from t_udm_estado;
delete from t_udm_estado_civil;
delete from t_udm_nivel_estudio;
delete from t_udm_tipo_enfermedad;
delete from t_udm_tipo_cancer;
delete from t_udm_tipo_estudio;
delete from t_udm_tipo_examen;
delete from t_udm_tipo_antecedente;

insert into t_udm_estado (id, nombre) values (1, 'Amazonas');
insert into t_udm_estado (id, nombre) values (2, 'Delta Amacuro');
insert into t_udm_estado (id, nombre) values (1000, 'Distrito Federal');
insert into t_udm_estado (id, nombre) values (1001, 'Miranda');
insert into t_udm_estado (id, nombre) values (1004, 'Carabobo');
insert into t_udm_estado (id, nombre) values (1005, 'Aragua');
insert into t_udm_estado (id, nombre) values (1006, 'Apure');
insert into t_udm_estado (id, nombre) values (1020, 'Sucre');
insert into t_udm_estado (id, nombre) values (1040, 'Portugueza');
insert into t_udm_estado (id, nombre) values (1060, 'Vargas');
insert into t_udm_estado (id, nombre) values (1080, 'Barcelona');
insert into t_udm_estado (id, nombre) values (1100, 'Lara');
insert into t_udm_estado (id, nombre) values (1120, 'M�rida');
insert into t_udm_estado (id, nombre) values (1121, 'Zulia');
insert into t_udm_estado (id, nombre) values (1123, 'Tachira');
insert into t_udm_estado (id, nombre) values (1140, 'Barinas');
insert into t_udm_estado (id, nombre) values (1141, 'Falc�n');
insert into t_udm_estado (id, nombre) values (1142, 'Yaracuy');
insert into t_udm_estado (id, nombre) values (1144, 'Gu�rico');
insert into t_udm_estado (id, nombre) values (1145, 'Cojedes');
insert into t_udm_estado (id, nombre) values (1146, 'Bol�var');
insert into t_udm_estado (id, nombre) values (1161, 'Monagas');
insert into t_udm_estado (id, nombre) values (1160, 'Trujillo');
insert into t_udm_estado (id, nombre) values (1180, 'Nueva Esparta');

insert into t_udm_ciudad (id, nombre, estado_id) values (1, 'Caracas', 1000);
insert into t_udm_ciudad (id, nombre, estado_id) values (2, 'Caracas', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (3, 'Maracaibo', 1121);
insert into t_udm_ciudad (id, nombre, estado_id) values (4, 'Valencia', 1004);
insert into t_udm_ciudad (id, nombre, estado_id) values (5, 'Barquisimeto', 1100);
insert into t_udm_ciudad (id, nombre, estado_id) values (6, 'Maracay', 1005);
insert into t_udm_ciudad (id, nombre, estado_id) values (7, 'Ciudad Guayana', 1146);
insert into t_udm_ciudad (id, nombre, estado_id) values (8, 'San Crist�bal', 1123);
insert into t_udm_ciudad (id, nombre, estado_id) values (9, 'Matur�n', 1161);
insert into t_udm_ciudad (id, nombre, estado_id) values (10, 'Barcelona', 1080);
insert into t_udm_ciudad (id, nombre, estado_id) values (11, 'Ciudad Bol�var', 1146);
insert into t_udm_ciudad (id, nombre, estado_id) values (12, 'Cuman�', 1020);
insert into t_udm_ciudad (id, nombre, estado_id) values (13, 'Barinas', 1140);
insert into t_udm_ciudad (id, nombre, estado_id) values (14, 'Cabimas', 1121);
insert into t_udm_ciudad (id, nombre, estado_id) values (15, 'Punto Fijo', 1141);
insert into t_udm_ciudad (id, nombre, estado_id) values (16, 'Puerto La Cruz', 1080);
insert into t_udm_ciudad (id, nombre, estado_id) values (17, 'Guarenas', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (18, 'Los Teques', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (19, 'M�rida', 1120);
insert into t_udm_ciudad (id, nombre, estado_id) values (20, 'Ciudad Ojeda', 1121);
insert into t_udm_ciudad (id, nombre, estado_id) values (21, 'Guanare', 1040);
insert into t_udm_ciudad (id, nombre, estado_id) values (22, 'Turmero', 1005);
insert into t_udm_ciudad (id, nombre, estado_id) values (23, 'Coro', 1141);
insert into t_udm_ciudad (id, nombre, estado_id) values (24, 'Guatire', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (25, 'Puerto Cabello', 1004);
insert into t_udm_ciudad (id, nombre, estado_id) values (26, 'El Tigre', 1080);
insert into t_udm_ciudad (id, nombre, estado_id) values (27, 'Acarigua', 1040);
insert into t_udm_ciudad (id, nombre, estado_id) values (28, 'Carora', 1100);
insert into t_udm_ciudad (id, nombre, estado_id) values (29, 'Guacara', 1004);
insert into t_udm_ciudad (id, nombre, estado_id) values (30, 'Santa Teresa del Tuy', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (31, 'San Fernando de Apure', 1006);
insert into t_udm_ciudad (id, nombre, estado_id) values (32, 'Car�pano', 1020);
insert into t_udm_ciudad (id, nombre, estado_id) values (33, 'La Victoria', 1005);
insert into t_udm_ciudad (id, nombre, estado_id) values (34, 'Cabudare', 1100);
insert into t_udm_ciudad (id, nombre, estado_id) values (35, 'G�ig�e', 1004);
insert into t_udm_ciudad (id, nombre, estado_id) values (36, 'Villa de Cura', 1005);
insert into t_udm_ciudad (id, nombre, estado_id) values (37, 'Calabozo', 1144);
insert into t_udm_ciudad (id, nombre, estado_id) values (38, 'Araure', 1040);
insert into t_udm_ciudad (id, nombre, estado_id) values (39, 'Santa B�rbara del Zulia', 1121);
insert into t_udm_ciudad (id, nombre, estado_id) values (40, 'Santa Rita', 1005);
insert into t_udm_ciudad (id, nombre, estado_id) values (41, 'Ocumare del Tuy', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (42, 'Valera', 1160);
insert into t_udm_ciudad (id, nombre, estado_id) values (43, 'El Vig�a', 1120);
insert into t_udm_ciudad (id, nombre, estado_id) values (44, 'C�a', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (45, 'Machiques', 1121);
insert into t_udm_ciudad (id, nombre, estado_id) values (46, 'El Tocuyo', 1100);
insert into t_udm_ciudad (id, nombre, estado_id) values (47, 'San Juan de los Morros', 1144);
insert into t_udm_ciudad (id, nombre, estado_id) values (48, 'Anaco', 1080);
insert into t_udm_ciudad (id, nombre, estado_id) values (49, 'Valle de la Pascua', 1144);
insert into t_udm_ciudad (id, nombre, estado_id) values (50, 'Guasdualito', 1006);
insert into t_udm_ciudad (id, nombre, estado_id) values (51, 'Zaraza', 1144);
insert into t_udm_ciudad (id, nombre, estado_id) values (52, 'Santa Luc�a', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (53, 'Cagua', 1005);
insert into t_udm_ciudad (id, nombre, estado_id) values (54, 'T�riba', 1123);
insert into t_udm_ciudad (id, nombre, estado_id) values (55, 'Mariara', 1004);
insert into t_udm_ciudad (id, nombre, estado_id) values (56, 'La Concepci�n', 1121);
insert into t_udm_ciudad (id, nombre, estado_id) values (57, 'Upata', 1146);
insert into t_udm_ciudad (id, nombre, estado_id) values (58, 'Ejido', 1120);
insert into t_udm_ciudad (id, nombre, estado_id) values (59, 'San Felipe', 1142);
insert into t_udm_ciudad (id, nombre, estado_id) values (60, 'Qu�bor', 1100);
insert into t_udm_ciudad (id, nombre, estado_id) values (61, 'San Carlos', 1145);
insert into t_udm_ciudad (id, nombre, estado_id) values (62, 'Charallave', 1001);
insert into t_udm_ciudad (id, nombre, estado_id) values (63, 'Puerto Ayacucho', 1);
insert into t_udm_ciudad (id, nombre, estado_id) values (64, 'El Lim�n', 1005);
insert into t_udm_ciudad (id, nombre, estado_id) values (65, 'Caicara del Orinoco', 1146);
insert into t_udm_ciudad (id, nombre, estado_id) values (66, 'Tinaquillo', 1145);
insert into t_udm_ciudad (id, nombre, estado_id) values (67, 'Yaritagua', 1142);
insert into t_udm_ciudad (id, nombre, estado_id) values (68, 'Tucupita', 2);
insert into t_udm_ciudad (id, nombre, estado_id) values (69, 'Porlamar', 1180);
insert into t_udm_ciudad (id, nombre, estado_id) values (70, 'Los Puertos de Altagracia', 1121);
insert into t_udm_ciudad (id, nombre, estado_id) values (71, 'La Guaira', 1060);

insert into t_udm_institucion (id, nombre) values (1, 'Hospital de Ni�os JM de los R�os');
insert into t_udm_institucion (id, nombre) values (2, 'Fundaci�n Jacinto Convit');

insert into t_udm_estado_civil (nombre) values ('Soltero');
insert into t_udm_estado_civil (nombre) values ('Casado');
insert into t_udm_estado_civil (nombre) values ('Divorciado');
insert into t_udm_estado_civil (nombre) values ('Viudo');
insert into t_udm_estado_civil (nombre) values ('Concubinato');

insert into t_udm_nivel_estudio (nombre) values ('Pre-escolar');
insert into t_udm_nivel_estudio (nombre) values ('B�sica I (1ro, 2do...6to)');
insert into t_udm_nivel_estudio (nombre) values ('B�sica II (7mo, 8vo, 9no)');
insert into t_udm_nivel_estudio (nombre) values ('Media (4to, 5to)');
insert into t_udm_nivel_estudio (nombre) values ('Superior (Pregrado, Universitario, Postgrado)');

insert into t_udm_unidad (nombre) values ('Anatom�a Patol�gica');
insert into t_udm_unidad (nombre) values ('Gastroenterolog�a');
insert into t_udm_unidad (nombre) values ('Hematolog�a');
insert into t_udm_unidad (nombre) values ('Infectolog�a');
insert into t_udm_unidad (nombre) values ('Oncolog�a');

insert into t_udm_tipo_cancer (nombre, orden) values ('C�lon', 1);
insert into t_udm_tipo_cancer (nombre, orden) values ('Cuello Uterino', 2);
insert into t_udm_tipo_cancer (nombre, orden) values ('Laringe', 3);
insert into t_udm_tipo_cancer (nombre, orden) values ('Leucemia', 4);
insert into t_udm_tipo_cancer (nombre, orden) values ('Mama', 5);
insert into t_udm_tipo_cancer (nombre, orden) values ('Pr�stata', 6);
insert into t_udm_tipo_cancer (nombre, orden) values ('Pulm�n', 7);
insert into t_udm_tipo_cancer (nombre, orden) values ('Vejiga', 8);
insert into t_udm_tipo_cancer (nombre, orden) values ('Otro', 9);

insert into t_udm_tipo_enfermedad (nombre, orden) values ('Dengue', 1);
insert into t_udm_tipo_enfermedad (nombre, orden) values ('Tuberculosis', 2);
insert into t_udm_tipo_enfermedad (nombre, orden) values ('Meningitis', 3);
insert into t_udm_tipo_enfermedad (nombre, orden) values ('Papiloma', 4);
insert into t_udm_tipo_enfermedad (nombre, orden) values ('Neumon�a', 5);
insert into t_udm_tipo_enfermedad (nombre, orden) values ('Diarrea', 6);
insert into t_udm_tipo_enfermedad (nombre, orden) values ('Enfermedades Respiratorias', 7);
insert into t_udm_tipo_enfermedad (nombre, orden) values ('Otra', 8);

insert into t_udm_tipo_antecedente (nombre, orden) values ('Di�betes Tipo I', 1);
insert into t_udm_tipo_antecedente (nombre, orden) values ('Di�betes Tipo II', 2);
insert into t_udm_tipo_antecedente (nombre, orden) values ('Enfermedades Renales', 3);
insert into t_udm_tipo_antecedente (nombre, orden) values ('Enfermedades Inmunol�gicas', 4);
insert into t_udm_tipo_antecedente (nombre, orden) values ('Enfermedades Hematol�gicas', 5);
insert into t_udm_tipo_antecedente (nombre, orden) values ('Enfermedades Oncol�gicas', 6);
insert into t_udm_tipo_antecedente (nombre, orden) values ('Enfermedades Card�acas', 7);

insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Metilaci�n del gen MGMT', 'C', 1);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Detecci�n del gen n-MYC', 'C', 2);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Cuantificaci�n del gen n-MYC', 'C', 3);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Detecci�n de Virus Dengue', 'O', 4);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Detecci�n de Mycobacterium tuberculosis', 'O', 5);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Detecci�n del Virus Papiloma Humano', 'O', 6);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Meningitis', 'O', 7);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Diarrea por pat�genos', 'O', 8);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Neumon�a', 'O', 9);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Enfermedad respiratoria viral', 'O', 10);
insert into t_udm_tipo_examen (nombre, tipo, orden) values ('Chagas', 'O', 11);

insert into t_udm_tipo_estudio (nombre, orden) values ('Hematolog�a', 1);
insert into t_udm_tipo_estudio (nombre, orden) values ('Qu�mica', 2);
insert into t_udm_tipo_estudio (nombre, orden) values ('Heces', 3);
insert into t_udm_tipo_estudio (nombre, orden) values ('Orina', 4);
insert into t_udm_tipo_estudio (nombre, orden) values ('Serolog�a', 5);
insert into t_udm_tipo_estudio (nombre, orden) values ('Marcadores', 6);
insert into t_udm_tipo_estudio (nombre, orden) values ('Tejido (Biopsia)', 7);



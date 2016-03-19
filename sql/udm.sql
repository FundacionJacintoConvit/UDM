/*==============================================================*/
/* DBMS name:      PostgreSQL 7.3                               */
/* Created on:     2/15/2016 9:25:50 PM                         */
/*==============================================================*/


drop table T_UDM_CIUDAD;

drop table T_UDM_DIAGNOSTICO;

drop table T_UDM_DIAGNOSTICO_ANTECEDENTE;

drop table T_UDM_DIAGNOSTICO_ESTUDIO;

drop table T_UDM_DIAGNOSTICO_EXAMEN;

drop table T_UDM_DIAGNOSTICO_MEDICAMENTO;

drop table T_UDM_DIAGNOSTICO_SINTOMA;

drop table T_UDM_DIAGNOSTICO_TRASL_MUESTRA;

drop table T_UDM_ESTADO;

drop table T_UDM_ESTADO_CIVIL;

drop table T_UDM_INSTITUCION;

drop table T_UDM_NIVEL_ESTUDIO;

drop table T_UDM_PACIENTE;

drop table T_UDM_TIPO_ANTECEDENTE;

drop table T_UDM_TIPO_CANCER;

drop table T_UDM_TIPO_ENFERMEDAD;

drop table T_UDM_TIPO_ESTUDIO;

drop table T_UDM_TIPO_EXAMEN;

drop table T_UDM_UNIDAD;

drop table T_UDM_USUARIO;

drop table T_UDM_USUARIO_GROUPS;

drop table T_UDM_USUARIO_USER_PERMISSIONS;

drop sequence S_UDM_CIUDAD;

drop sequence S_UDM_DIAGNOSTICO;

drop sequence S_UDM_DIAGNOSTICO_ANTECEDENTE;

drop sequence S_UDM_DIAGNOSTICO_ESTUDIO;

drop sequence S_UDM_DIAGNOSTICO_MEDICAMENTO;

drop sequence S_UDM_DIAGNOSTICO_RESULTADO;

drop sequence S_UDM_DIAGNOSTICO_SINTOMA;

drop sequence S_UDM_DIAGNOSTICO_TRASL_MUESTRA;

drop sequence S_UDM_ESTADO;

drop sequence S_UDM_ESTADO_CIVIL;

drop sequence S_UDM_INSTITUCION;

drop sequence S_UDM_NIVEL_ESTUDIO;

drop sequence S_UDM_PACIENTE;

drop sequence S_UDM_TIPO_ANTECEDENTE;

drop sequence S_UDM_TIPO_CANCER;

drop sequence S_UDM_TIPO_ENFERMEDAD;

drop sequence S_UDM_TIPO_ESTUDIO;

drop sequence S_UDM_TIPO_EXAMEN;

drop sequence S_UDM_UNIDAD;

drop sequence S_UDM_USUARIO;

drop sequence S_UDM_USUARIO_GROUPS;

drop sequence S_UDM_USUARIO_USER_PERMISSIONS;

create sequence S_UDM_CIUDAD
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_DIAGNOSTICO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_DIAGNOSTICO_ANTECEDENTE
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_DIAGNOSTICO_ESTUDIO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_DIAGNOSTICO_MEDICAMENTO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_DIAGNOSTICO_RESULTADO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_DIAGNOSTICO_SINTOMA
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_DIAGNOSTICO_TRASL_MUESTRA
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_ESTADO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_ESTADO_CIVIL
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_INSTITUCION
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_NIVEL_ESTUDIO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_PACIENTE
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_TIPO_ANTECEDENTE
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_TIPO_CANCER
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_TIPO_ENFERMEDAD
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_TIPO_ESTUDIO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_TIPO_EXAMEN
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_UNIDAD
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_USUARIO
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_USUARIO_GROUPS
minvalue 1000
start 1000
cache 1;

create sequence S_UDM_USUARIO_USER_PERMISSIONS
minvalue 1000
start 1000
cache 1;

/*==============================================================*/
/* Table: T_UDM_CIUDAD                                          */
/*==============================================================*/
create table T_UDM_CIUDAD (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
ESTADO_ID            INT8                 not null,
constraint PK_UDM_CIUDAD primary key (ID),
constraint AK_UDM_CIUDAD unique (NOMBRE, ESTADO_ID)
);

/*==============================================================*/
/* Table: T_UDM_DIAGNOSTICO                                     */
/*==============================================================*/
create table T_UDM_DIAGNOSTICO (
ID                   SERIAL not null,
MEDICO_TIPO_DIAGNOSTICO CHAR(1)              null,
MEDICO_FECHA_INI_SINTOMAS DATE                 null,
MEDICO_FECHA_FIN_SINTOMAS DATE                 null,
MEDICO_FECHA_INI_SIGNOS DATE                 null,
MEDICO_FECHA_FIN_SIGNOS DATE                 null,
MEDICO_SIGNOS        VARCHAR(4000)        null,
MEDICO_SINTOMAS      VARCHAR(4000)        null,
MEDICO_DIAGNOSTICO_PRESUNTIVO VARCHAR(4000)        null,
MEDICO_PRESENCIA_TUMOR CHAR(1)              null,
MEDICO_UBICACION_TUMOR VARCHAR(4000)        null,
MEDICO_PRESENCIA_METASTASIS CHAR(1)              null,
MEDICO_UBICACION_METASTASIS VARCHAR(4000)        null,
MEDICO_OTROS_ESTUDIOS VARCHAR(4000)        null,
MEDICO_OBSERVACIONES VARCHAR(4000)        null,
MEDICO_FAMILIAR_ANTECEDENTE BOOL                 null,
MEDICO_FAMILIAR_NEXO VARCHAR(255)         null,
MEDICO_FAMILIAR_TIPO_ENFERM_ID INT8                 null,
MEDICO_FAMILIAR_TIPO_CANCER_ID INT8                 null,
MEDICO_FAMILIAR_ENFERMEDAD_OTRA VARCHAR(255)         null,
MEDICO_UBICACION_INSTITUCION_ID INT8                 null,
MEDICO_UBICACION_TELEFONO VARCHAR(255)         null,
MEDICO_UBICACION_PISO NUMERIC(3)           null,
MEDICO_UBICACION_HABITACION VARCHAR(255)         null,
MEDICO_PACIENTE_CUMPLIO_COND CHAR(1)              null,
MEDICO_PACIENTE_CUMPLIO_AYUNO12 BOOL                 null,
MEDICO_PACIENTE_CUMPLIO_AYUNO3 BOOL                 null,
MEDICO_PACIENTE_CUMPLIO_OBSERVA VARCHAR(4000)        null,
PATOLOGO_TIPO_MUESTRA VARCHAR(4000)        null,
PATOLOGO_RESULTADO   VARCHAR(4000)        null,
PATOLOGO_MARCADORES  VARCHAR(4000)        null,
PATOLOGO_OBSERVACIONES VARCHAR(4000)        null,
UDM_OBSERVACIONES    VARCHAR(4000)        null,
UDM_TIPO_MUESTRA     VARCHAR(255)         null,
UDM_TIPO_MUESTRA_OTRO VARCHAR(255)         null,
UDM_TECNICA_DETECCION VARCHAR(255)         null,
CREACION_FECHA       TIMESTAMP            null,
MEDICO_MODIFICACION_FECHA TIMESTAMP            null,
PATOLOGO_MODIFICACION_FECHA TIMESTAMP            null,
UDM_MODIFICACION_FECHA TIMESTAMP            null,
PACIENTE_ID          INT8                 not null,
CREACION_USUARIO_ID  INT8                 null,
MEDICO_MODIFICACION_USUARIO_ID INT8                 null,
PATOLOGO_MODIFICACION_USUARIO_I INT8                 null,
UDM_MODIFICACION_USUARIO_ID INT8                 null,
constraint PK_UDM_DIAGNOSTICO primary key (ID)
);

/*==============================================================*/
/* Table: T_UDM_DIAGNOSTICO_ANTECEDENTE                         */
/*==============================================================*/
create table T_UDM_DIAGNOSTICO_ANTECEDENTE (
ID                   SERIAL not null,
OTRO                 BOOL                 null,
PRESENTE             BOOL                 null,
ANTECEDENTE          VARCHAR(255)         null,
NEXO_FAMILIAR        VARCHAR(255)         null,
ORDEN                INT8                 null,
DIAGNOSTICO_ID       INT8                 null,
TIPO_ANTECEDENTE_ID  INT8                 null,
constraint PK_T_UDM_DIAGNOSTICO_ANTECEDEN primary key (ID)
);

/*==============================================================*/
/* Table: T_UDM_DIAGNOSTICO_ESTUDIO                             */
/*==============================================================*/
create table T_UDM_DIAGNOSTICO_ESTUDIO (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
LINK                 VARCHAR(255)         null,
RUTA                 VARCHAR(255)         null,
ORDEN                INT8                 null,
DIAGNOSTICO_ID       INT8                 null,
TIPO_ESTUDIO_ID      INT8                 null,
constraint PK_UDM_DIAGNOSTICO_ESTUDIO primary key (ID)
);

/*==============================================================*/
/* Table: T_UDM_DIAGNOSTICO_EXAMEN                              */
/*==============================================================*/
create table T_UDM_DIAGNOSTICO_EXAMEN (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
PRESENTE             BOOL                 null,
RESULTADO            BOOL                 null,
TIPO                 VARCHAR(255)         null,
ORDEN                INT8                 null,
DIAGNOSTICO_ID       INT8                 null,
TIPO_EXAMEN_ID       INT8                 null,
constraint PK_UDM_DIAGNOSTICO_RESULTADO primary key (ID),
constraint AK_UDM_DIAGNOSTICO_RESULTADO unique (NOMBRE, DIAGNOSTICO_ID)
);

/*==============================================================*/
/* Table: T_UDM_DIAGNOSTICO_MEDICAMENTO                         */
/*==============================================================*/
create table T_UDM_DIAGNOSTICO_MEDICAMENTO (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
FECHA_INICIO         DATE                 null,
DOSIS                VARCHAR(255)         null,
INDICACION           VARCHAR(4000)        null,
DIAGNOSTICO_ID       INT8                 null,
constraint PK_UDM_DIAGNOSTICO_MEDICAMENTO primary key (ID),
constraint AK_UDM_DIAGNOSTICO_MEDICAMENTO unique (NOMBRE, DIAGNOSTICO_ID)
);

/*==============================================================*/
/* Table: T_UDM_DIAGNOSTICO_SINTOMA                             */
/*==============================================================*/
create table T_UDM_DIAGNOSTICO_SINTOMA (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
PRESENTE             BOOL                 null,
CUANTOS              NUMERIC(3)           null,
PERSONAS             VARCHAR(255)         null,
TIPOS                VARCHAR(255)         null,
ORDEN                INT8                 null,
DIAGNOSTICO_ID       INT8                 null,
constraint PK_UDM_DIAGNOSTICO_SINTOMA primary key (ID),
constraint AK_UDM_DIAGNOSTICO_SINTOMA unique (NOMBRE, DIAGNOSTICO_ID)
);

/*==============================================================*/
/* Table: T_UDM_DIAGNOSTICO_TRASL_MUESTRA                       */
/*==============================================================*/
create table T_UDM_DIAGNOSTICO_TRASL_MUESTRA (
ID                   SERIAL not null,
RUTA                 VARCHAR(255)         not null,
ORDEN                INT8                 null,
DIAGNOSTICO_ID       INT8                 null,
constraint PK_T_UDM_DIAGNOSTICO_TRASL_MUE primary key (ID),
constraint AK_AK_UDM_ESTADO_CIVI_T_UDM_DI unique (RUTA)
);

/*==============================================================*/
/* Table: T_UDM_ESTADO                                          */
/*==============================================================*/
create table T_UDM_ESTADO (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
constraint PK_UDM_ESTADO primary key (ID),
constraint AK_UDM_ESTADO unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_ESTADO_CIVIL                                    */
/*==============================================================*/
create table T_UDM_ESTADO_CIVIL (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
constraint PK_T_UDM_ESTADO_CIVIL primary key (ID),
constraint AK_AK_UDM_ESTADO_CIVI_T_UDM_ES unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_INSTITUCION                                     */
/*==============================================================*/
create table T_UDM_INSTITUCION (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
constraint PK_T_UDM_INSTITUCION primary key (ID),
constraint AK_AK_UDM_INSTITUCION_T_UDM_IN unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_NIVEL_ESTUDIO                                   */
/*==============================================================*/
create table T_UDM_NIVEL_ESTUDIO (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
constraint PK_T_UDM_NIVEL_ESTUDIO primary key (ID),
constraint AK_AK_UDM_ESTADO_CIVI_T_UDM_NI unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_PACIENTE                                        */
/*==============================================================*/
create table T_UDM_PACIENTE (
ID                   SERIAL not null,
NOMBRE_PRIMERO       VARCHAR(255)         not null,
NOMBRE_SEGUNDO       VARCHAR(255)         null,
APELLIDO_PRIMERO     VARCHAR(255)         not null,
APELLIDO_SEGUNDO     VARCHAR(255)         null,
TIPO_IDENTIFICACION  CHAR(1)              null,
IDENTIFICACION       VARCHAR(20)          null,
PARTIDA_NACIMIENTO   VARCHAR(255)         null,
FECHA_NACIMIENTO     DATE                 null,
EDAD_ANIOS           NUMERIC(3)           null,
EDAD_MESES           NUMERIC(3)           null,
SEXO                 CHAR(1)              null,
NACIONALIDAD         CHAR(1)              null,
REPRESENT_NOMBRE_PRIMERO VARCHAR(255)         null,
REPRESENT_NOMBRE_SEGUNDO VARCHAR(255)         null,
REPRESENT_APELLIDO_PRIMERO VARCHAR(255)         null,
REPRESENT_APELLIDO_SEGUNDO VARCHAR(255)         null,
REPRESENT_TIPO_IDENTIFICACION CHAR(1)              null,
REPRESENT_IDENTIFICACION VARCHAR(20)          null,
REPRESENT_NUMERO_HIJO NUMERIC(3)           null,
REPRESENT_SEXO       CHAR(1)              null,
REPRESENT_FECHA_NACIMIENTO DATE                 null,
REPRESENT_NACIONALIDAD CHAR(1)              null,
TELEFONO_LOCAL       VARCHAR(255)         null,
TELEFONO_CELULAR1    VARCHAR(255)         null,
TELEFONO_CELULAR2    VARCHAR(255)         null,
CORREO_ELECTRONICO   VARCHAR(255)         null,
CALLE_AVENIDA        VARCHAR(255)         null,
SECTOR_BARRIO_URB    VARCHAR(255)         null,
CASA_EDIFICIO        VARCHAR(255)         null,
FAMILIARES_OBSERVACIONES VARCHAR(4000)        null,
NUMERO_HISTORIA      VARCHAR(255)         null,
CIUDAD_ID            INT8                 not null,
ESTADO_CIVIL_ID      INT8                 null,
NIVEL_ESTUDIO_ID     INT8                 null,
REPRESENT_ESTADO_CIVIL_ID INT8                 null,
REPRESENT_NIVEL_ESTUDIO_ID INT8                 null,
constraint PK_UDM_PACIENTE primary key (ID)
);

/*==============================================================*/
/* Table: T_UDM_TIPO_ANTECEDENTE                                */
/*==============================================================*/
create table T_UDM_TIPO_ANTECEDENTE (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
ORDEN                INT8                 not null,
constraint PK_T_UDM_TIPO_ANTECEDENTE primary key (ID),
constraint AK_AK_UDM_TIPO_ANTECE_T_UDM_TI unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_TIPO_CANCER                                     */
/*==============================================================*/
create table T_UDM_TIPO_CANCER (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
ORDEN                INT8                 not null,
constraint PK_T_UDM_TIPO_CANCER primary key (ID),
constraint AK_AK_UDM_TIPO_CANCER_T_UDM_TI unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_TIPO_ENFERMEDAD                                 */
/*==============================================================*/
create table T_UDM_TIPO_ENFERMEDAD (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
ORDEN                INT8                 not null,
constraint PK_T_UDM_TIPO_ENFERMEDAD primary key (ID),
constraint AK_AK_UDM_TIPO_ENFERM_T_UDM_TI unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_TIPO_ESTUDIO                                    */
/*==============================================================*/
create table T_UDM_TIPO_ESTUDIO (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
ORDEN                INT8                 not null,
constraint PK_T_UDM_TIPO_ESTUDIO primary key (ID),
constraint AK_AK_UDM_TIPO_ESTUDI_T_UDM_TI unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_TIPO_EXAMEN                                     */
/*==============================================================*/
create table T_UDM_TIPO_EXAMEN (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
TIPO                 VARCHAR(255)         not null,
ORDEN                INT8                 not null,
constraint PK_T_UDM_TIPO_EXAMEN primary key (ID),
constraint AK_AK_UDM_TIPO_EXAMEN_T_UDM_TI unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_UNIDAD                                          */
/*==============================================================*/
create table T_UDM_UNIDAD (
ID                   SERIAL not null,
NOMBRE               VARCHAR(255)         not null,
constraint PK_T_UDM_UNIDAD primary key (ID),
constraint AK_AK_UDM_UNIDAD_T_UDM_UN unique (NOMBRE)
);

/*==============================================================*/
/* Table: T_UDM_USUARIO                                         */
/*==============================================================*/
create table T_UDM_USUARIO (
ID                   SERIAL not null,
PASSWORD             VARCHAR(128)         not null,
LAST_LOGIN           TIMESTAMP WITH TIME ZONE null,
IS_SUPERUSER         BOOL                 not null,
USERNAME             VARCHAR(30)          not null,
FIRST_NAME           VARCHAR(30)          not null,
LAST_NAME            VARCHAR(30)          not null,
EMAIL                VARCHAR(75)          not null,
IS_STAFF             BOOL                 not null,
IS_ACTIVE            BOOL                 not null,
DATE_JOINED          TIMESTAMP WITH TIME ZONE not null,
TELEFONO             VARCHAR(255)         null,
CIUDAD_ID            INT8                 null,
INSTITUCION_ID       INT8                 null,
FIRMA                VARCHAR(255)         null,
NOMBRE_SEGUNDO       VARCHAR(255)         null,
APELLIDO_SEGUNDO     VARCHAR(255)         null,
NACIONALIDAD         CHAR(1)              null,
CEDULA_PASAPORTE     VARCHAR(255)         null,
EDAD                 INTEGER              null,
SEXO                 CHAR(1)              null,
PROFESION            VARCHAR(255)         null,
ESPECIALIZACION      VARCHAR(255)         null,
ESPECIALIZACION_CULMINADA CHAR(1)              null,
NUMERO_MPPS          VARCHAR(255)         null,
NUMERO_COLEGIO       VARCHAR(255)         null,
UBICACION_COLEGIO    VARCHAR(255)         null,
UNIDAD_FECHA_INICIO  DATE                 null,
UNIDAD_FECHA_FIN     DATE                 null,
UNIDAD_DIRECTOR      VARCHAR(255)         null,
UNIDAD_DIRECTOR_TELEFONO VARCHAR(255)         null,
UNIDAD_DIRECTOR_EMAIL VARCHAR(255)         null,
UNIDAD_ID            INT8                 null,
constraint PK_T_UDM_USUARIO primary key (ID)
);

/*==============================================================*/
/* Table: T_UDM_USUARIO_GROUPS                                  */
/*==============================================================*/
create table T_UDM_USUARIO_GROUPS (
ID                   SERIAL not null,
UDMUSER_ID           INT8                 not null,
GROUP_ID             INT8                 not null,
constraint PK_T_UDM_USUARIO_GROUPS primary key (ID)
);

/*==============================================================*/
/* Table: T_UDM_USUARIO_USER_PERMISSIONS                        */
/*==============================================================*/
create table T_UDM_USUARIO_USER_PERMISSIONS (
ID                   SERIAL not null,
UDMUSER_ID           INT8                 not null,
PERMISSION_ID        INT8                 not null,
constraint PK_T_UDM_USUARIO_USER_PERMISSI primary key (ID)
);

alter table T_UDM_CIUDAD
   add constraint FK_UDM_ESTADO_CIUDAD foreign key (ESTADO_ID)
      references T_UDM_ESTADO (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO
   add constraint FK_UDM_DIAGNOSTICO_PACIENTE foreign key (PACIENTE_ID)
      references T_UDM_PACIENTE (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO
   add constraint FK_UDM_DIAGNOSTICO_TIPO_CANCER foreign key (MEDICO_FAMILIAR_TIPO_CANCER_ID)
      references T_UDM_TIPO_CANCER (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO
   add constraint FK_UDM_DIAGNOSTICO_TIPO_ENFERM foreign key (MEDICO_FAMILIAR_TIPO_ENFERM_ID)
      references T_UDM_TIPO_ENFERMEDAD (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_ANTECEDENTE
   add constraint FK_UDM_DIAGNOSTICO_ANTECEDENTE1 foreign key (DIAGNOSTICO_ID)
      references T_UDM_DIAGNOSTICO (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_ANTECEDENTE
   add constraint FK_UDM_DIAGNOSTICO_ANTECEDENTE2 foreign key (TIPO_ANTECEDENTE_ID)
      references T_UDM_TIPO_ANTECEDENTE (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_ESTUDIO
   add constraint FK_UDM_DIAGNOSTICO_ESTUDIO foreign key (DIAGNOSTICO_ID)
      references T_UDM_DIAGNOSTICO (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_ESTUDIO
   add constraint FK_UDM_DIAGNOSTICO_TIPO_ESTUDIO foreign key (TIPO_ESTUDIO_ID)
      references T_UDM_TIPO_ESTUDIO (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_EXAMEN
   add constraint FK_UDM_DIAGNOSTICO_RESULTADO foreign key (DIAGNOSTICO_ID)
      references T_UDM_DIAGNOSTICO (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_EXAMEN
   add constraint FK_UDM_DIAGNOSTICO_TIPO_EXAMEN foreign key (TIPO_EXAMEN_ID)
      references T_UDM_TIPO_EXAMEN (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_MEDICAMENTO
   add constraint FK_UDM_DIAGNOSTICO_MEDICAMENTO foreign key (DIAGNOSTICO_ID)
      references T_UDM_DIAGNOSTICO (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_SINTOMA
   add constraint FK_UDM_DIAGNOSTICO_SINTOMA foreign key (DIAGNOSTICO_ID)
      references T_UDM_DIAGNOSTICO (ID)
      on delete restrict on update restrict;

alter table T_UDM_DIAGNOSTICO_TRASL_MUESTRA
   add constraint FK_UDM_DIAGNOSTICO_TRAS_MUESTRA foreign key (DIAGNOSTICO_ID)
      references T_UDM_DIAGNOSTICO (ID)
      on delete restrict on update restrict;

alter table T_UDM_PACIENTE
   add constraint FK_UDM_CIUDAD_PACIENTE foreign key (CIUDAD_ID)
      references T_UDM_CIUDAD (ID)
      on delete restrict on update restrict;

alter table T_UDM_PACIENTE
   add constraint FK_UDM_PACIENTE_ESTADO_CIVIL foreign key (ESTADO_CIVIL_ID)
      references T_UDM_ESTADO_CIVIL (ID)
      on delete restrict on update restrict;

alter table T_UDM_PACIENTE
   add constraint FK_UDM_PACIENTE_NIVEL_ESTUDIO foreign key (NIVEL_ESTUDIO_ID)
      references T_UDM_NIVEL_ESTUDIO (ID)
      on delete restrict on update restrict;

alter table T_UDM_PACIENTE
   add constraint FK_UDM_REPRESENT_ESTADO_CIVIL foreign key (REPRESENT_ESTADO_CIVIL_ID)
      references T_UDM_ESTADO_CIVIL (ID)
      on delete restrict on update restrict;

alter table T_UDM_PACIENTE
   add constraint FK_UDM_REPRESENT_NIVEL_ESTUDIO foreign key (REPRESENT_NIVEL_ESTUDIO_ID)
      references T_UDM_NIVEL_ESTUDIO (ID)
      on delete restrict on update restrict;

alter table T_UDM_USUARIO
   add constraint FK_UDM_USUARIO_CIUDAD foreign key (CIUDAD_ID)
      references T_UDM_CIUDAD (ID)
      on delete restrict on update restrict;

alter table T_UDM_USUARIO
   add constraint FK_UDM_USUARIO_INSTITUCION foreign key (INSTITUCION_ID)
      references T_UDM_INSTITUCION (ID)
      on delete restrict on update restrict;

alter table T_UDM_USUARIO
   add constraint FK_UDM_USUARIO_UNIDAD foreign key (UNIDAD_ID)
      references T_UDM_UNIDAD (ID)
      on delete restrict on update restrict;

alter table T_UDM_USUARIO_GROUPS
   add constraint FK_UDM_USUARIO_GROUPS foreign key (UDMUSER_ID)
      references T_UDM_USUARIO (ID)
      on delete restrict on update restrict;

alter table T_UDM_USUARIO_USER_PERMISSIONS
   add constraint FK_UDM_USUARIO_USER_PERMISSIONS foreign key (UDMUSER_ID)
      references T_UDM_USUARIO (ID)
      on delete restrict on update restrict;


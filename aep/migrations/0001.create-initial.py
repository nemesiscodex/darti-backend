from yoyo import step

steps = [
    step(
        """
        create table area
        (
            id serial not null constraint area_pk primary key,
            identifier serial not null,
            latitude varchar(30) not null,
            longitude varchar(30) not null,
            name varchar(100) not null,
            area_type varchar(100) not null,
            parent_area_identifier int
        );
        
        create index area_area_type_index on area (area_type);
        
        create unique index area_identifier_uindex
        on area (identifier);
        
        create index area_parent_area_identifier_index
        on area (parent_area_identifier);
        
        create table sensor
        (
            id serial not null
                constraint sensor_pk
                    primary key,
            identifier int not null,
            latitude varchar(30) not null,
            longitude varchar(30) not null,
            area_identifier int,
            sensor_type varchar(100) not null
        );
        
        create index sensor_area_identifier_index
        on sensor (area_identifier);
        
        create unique index sensor_identifier_uindex
        on sensor (identifier);
        
        create index sensor_sensor_type_index
        on sensor (sensor_type);
        
        create table reading
        (
            id serial not null
                constraint reading_pk
                    primary key,
            identifier serial not null,
            timestamp timestamp default now() not null,
            latitude varchar(30) not null,
            longitude varchar(30) not null,
            wind_direction numeric not null,
            wind_velocity numeric not null,
            rainfall numeric not null,
            interior_temperature numeric not null,
            exterior_temperature numeric not null,
            humidity numeric not null,
            atmospheric_pressure numeric not null
        );
        
        create unique index reading_identifier_uindex
        on reading (identifier);
        
        create index reading_timestamp_index
        on reading (timestamp desc);
        
        create table activation
        (
            id serial not null
                constraint activation_pk
                    primary key,
            identifier serial not null,
            reading_identifier int not null,
            activation_count int not null,
            sensor_identifier int not null
        );
        
        create unique index activation_identifier_uindex
        on activation (identifier);
        
        create index activation_reading_identifier_index
        on activation (reading_identifier);
        
        create index activation_sensor_identifier_index
        on activation (sensor_identifier);
        """,
        ignore_errors='apply'
    ),
]

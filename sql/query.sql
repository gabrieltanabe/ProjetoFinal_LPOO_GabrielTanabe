create table if not exists tb_filmes(
    id_filme serial primary key,
    titulo varchar(150) not null,
    duracao integer not null check (duracao > 0),
    classificacao varchar(50) not null,
    status varchar(50) not null
);

create table if not exists tb_salas(
    id_sala serial primary key,
    numero integer not null unique check (numero > 0),
    capacidade integer not null check (capacidade > 0)
);

create table if not exists tb_sessoes(
    id_sessao serial primary key,
    id_filme integer not null,
    id_sala integer not null,
    data_hora timestamp not null,
    preco_base numeric(10, 2) not null check (preco_base >= 0),
    status varchar(50) not null,
    constraint fk_sessao_filme foreign key (id_filme) references tb_filmes (id_filme) on delete cascade,
    constraint fk_sessao_sala foreign key (id_sala) references tb_salas (id_sala) on delete cascade
);

create table if not exists tb_ingressos(
    id_ingresso serial primary key,
    id_sessao integer not null,
    assento integer not null check (assento > 0),
    tipo varchar(50) not null,
    constraint fk_ingresso_sessao foreign key (id_sessao) references tb_sessoes (id_sessao) on delete cascade,
    constraint uq_sessao_assento unique (id_sessao, assento) -- garante que um assento não seja vendido duas vezes na mesma sessão
);

create table if not exists tb_vendas(
    id_venda serial primary key,
    id_ingresso integer not null unique, -- relação 1:1, um ingresso pertence a uma única venda
    metodo_pagamento varchar(50) not null,
    valor_total numeric(10, 2) not null check (valor_total >= 0),
    data_venda timestamp not null default current_timestamp,
    constraint fk_venda_ingresso foreign key (id_ingresso) references tb_ingressos (id_ingresso) on delete cascade
);

select * from tb_filmes;
select * from tb_salas;
select * from tb_sessoes;
select * from tb_ingressos;
select * from tb_vendas;

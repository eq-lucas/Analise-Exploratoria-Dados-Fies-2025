select count(*) as `qtdeLinhas`
from(
select count(*) as REPETICAO
from fies_2_inscricoes_2021_regular
group by  `ID do estudante`,`Opções de cursos da inscrição`
) as f;




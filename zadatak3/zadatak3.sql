--a
select municipality, count(*) as num
from realestate_db.realestate
where city = 'Beograd'
group by municipality
order by num desc
limit 8

--b
select squareFootage, sf.num
from (select "do 35 kvadrata" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage <= 35 and squareFootage > 0 and country = 'Srbija'
        union all
        select "36-50" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage <= 50 and squareFootage >= 36 and country = 'Srbija'
        union all
        select "51-65" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage <= 65 and squareFootage >= 51 and country = 'Srbija'
        union all
        select "66-80" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage <= 80 and squareFootage >= 66 and country = 'Srbija'
        union all
        select "80-95" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage <= 95 and squareFootage >= 80 and country = 'Srbija'
        union all
        select "96-110" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage <= 110 and squareFootage >= 96 and country = 'Srbija'
        union all
        select "111-140" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage <= 140 and squareFootage >= 111 and country = 'Srbija'
		union all
		select "141 kvadrata i vise" as squareFootage, count(*) as num 
		from realestate_db.realestate
		where type = 'flat' and typeOfOffer = 'sale' and squareFootage >= 141 and country = 'Srbija'
    ) sf;
	
--c
select constructionYear, year.num
from (select "1950-1959" as constructionYear, count(*) as num 
		from realestate_db.realestate
		where constructionYear <= 1959 and constructionYear >= 1950
        union all
        select "1960-1969" as constructionYear, count(*) as num 
		from realestate_db.realestate
		where constructionYear <= 1969 and constructionYear >= 1960
        union all
        select "1970-1979" as constructionYear, count(*) as num 
		from realestate_db.realestate
		where constructionYear <= 1979 and constructionYear >= 1970
        union all
        select "1980-1989" as constructionYear, count(*) as num 
		from realestate_db.realestate
		where constructionYear <= 1989 and constructionYear >= 1980
        union all
        select "1990-1999" as constructionYear, count(*) as num 
		from realestate_db.realestate
		where constructionYear <= 95 and constructionYear >= 80
        union all
        select "2000-2009" as constructionYear, count(*) as num 
		from realestate_db.realestate
		where constructionYear <= 2009 and constructionYear >= 2000
        union all
        select "2010-2019" as constructionYear, count(*) as num 
		from realestate_db.realestate
		where constructionYear <= 2019 and constructionYear >= 2010
    ) year;
	
--d
select C1.city, C1.broj as iznajmljivanje, C2.broj as prodaja
from
(select A1.city as city, A1.num as total, B1.num as broj
	from (select city, count(*) as num
		from realestate_db.realestate
		group by city
		order by num desc
		limit 8) A1 
        left join
        (select city, count(*) as num
			from realestate_db.realestate
			where  typeOfOffer = 'rent'
			group by city) B1
		on A1.city = B1.city) C1
	inner join
	(select A2.city as city, A2.num as total, B2.num as broj
	from (select city, count(*) as num
		from realestate_db.realestate
		group by city
		order by num desc
		limit 8) A2
        left join
        (select city, count(*) as num
			from realestate_db.realestate
			where  typeOfOffer = 'sale'
			group by city) B2
		on A2.city = B2.city) C2
        on C1.city = C2.city
group by city
		
--e
select price, pr.num as num
from (select "manje od 49 999 €" as price, count(*) as num 
		from realestate_db.realestate
		where price <= 4999 and typeOfOffer = 'sale'
        union all
        select "između 50 000 i 99 999 €" as price, count(*) as num 
		from realestate_db.realestate
		where  typeOfOffer = 'sale' and price <= 99999 and price >= 50000
        union all
        select "između 100 000 i 149 999 €" as price, count(*) as num 
		from realestate_db.realestate
		where price <= 149999 and price >= 100000 and typeOfOffer = 'sale'
        union all
        select "između 150 000 € i 199 999 €" as price, count(*) as num 
		from realestate_db.realestate
		where price <= 199999 and price >= 150000 and typeOfOffer = 'sale'
        union all
        select "200 000 € ili vise" as price, count(*) as num 
		from realestate_db.realestate
		where price >= 200000 and typeOfOffer = 'sale'
    ) pr;
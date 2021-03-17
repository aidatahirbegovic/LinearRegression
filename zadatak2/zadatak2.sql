--a
select typeOfOffer, count(*) as num
from realestate_db.realestate 
group by typeOfOffer

--b
select city, count(*) as num
from realestate_db.realestate 
group by city 

--c
select con, count(*) as num
from realestate_db.realestate
where con = 'Novogradnja' 
group by con

--d
(select *
from realestate_db.realestate 
where type = 'home' and typeOfOffer = 'sale'
group by idrealestate
order by price desc
limit 25)
union
(select *
from realestate_db.realestate 
where type = 'flat' and typeOfOffer = 'sale' and country = 'Srbija'
group by idrealestate
order by price desc
limit 25)
union
(select *
from realestate_db.realestate 
where type = 'cottage' and typeOfOffer = 'sale'
group by idrealestate
order by price desc
limit 20)

--e
(select *
from realestate_db.realestate 
where type = 'home' and typeOfOffer = 'rent' and city = 'Beograd'
group by idrealestate
order by price desc
limit 50)
union
(select *
from realestate_db.realestate 
where type = 'flat' and typeOfOffer = 'rent' and city = 'Beograd'
group by idrealestate
order by price desc
limit 50)

--f
select *
from realestate_db.realestate 
where constructionYear = '2019' or constructionYear = '2020'
group by idrealestate
order by price desc

--g1
select *
from realestate_db.realestate 
group by idrealestate
order by roomNo desc
limit 1

--g2
select *
from realestate_db.realestate where bathroomNo > 3
group by idrealestate 

--g3
select *
from realestate_db.realestate where pumpaIliKalorimetri = 'pumpa' or pumpaIliKalorimetri = 'kalorimetri'
group by idrealestate 

--g4
select *
from realestate_db.realestate where pl = 'yes'
group by idrealestate 
from brownie import *


def main(ve_zoo):

	active_network = network.show_active()
	account = accounts.load(active_network)

	collections = ["0x8C3c07B7Edd2F0BE5b4Ed8064Ec722Da57F9A9d2", # Alley Katz
	"0x62fA8dE3e52541e9e0cc07bf577e1BCEfD0aDAB6", # ALPACADABRAZ
	"0xF348800916C2e84c7B1630EB16FB0eFc52F3c235", # Dead Freaks
	"0x87C359d86bD8C794124090A82E0930c3Cab88F01", # Devious Demon Dudes
	"0x207F3F8ff92312DCB092f4087CdBeC3626E26cd4", # Dumspter Dorks S1
	"0xCd49e7b7515f053A07f2b577b6e87Cfd9B2589FC", # Dumpster Dorks S2
	"0xE665F4Cb94D176641E6c79f7dDcd7590d7cCb647", # ELVEN
	"0x6f126696447A2B32D9A3160f5bB734d039B67B5A", # Ethlizards
	"0x43DF558DE9F4619600956fF7AC1894F74d26BBc6", # Fancy Birds
	"0x357FbA23587e47C6Ed25f0B3650Ed3F86e046627", # FLUF World
	"0x81C60843A985636186CfdC8162Ec548c75aA42c9", # Fluffy Polar Bears
	"0xec17cD142795431B45b6FEce06B8b3682621A84C", # Holy Cows
	"0x3EdDc6f8C1cf8a6d7b95C456Bba80887226533AA", # Humans Of The Metaverse
	"0x80f7931E971317402002c1BE3B582867B9A24828", # Lobby Lobsters
	"0xE9fDF067327411AaE71D6869631767926f600Ac6", # Luchadores
	"0xd0F8F69FF554f4bDb1fF0c877DaFEbF74628E791", # Meta Eagle Club
	"0x8953356fb37cee93C601c48B249264923B2fFf66", # MetaTravelers
	"0xC27FB62c388Ac0f5e55B91D6491f4f469e56Bf71", # Monster Shelter
	"0x6ec049DB1142a51F13967A2C04143255CC99410C", # MoonCats
	"0xe5d6806396d4679Ab21D4BaB3fb5e724Fe82f6a0", # PixaWizards
	"0x958B6289e048C5BC21F3c9c61e58022d2358d06F", # Polymorphs
	"0xf25a1CF5be78A1C57b306Ad5999F255bFd2d9225", # Purr Evil
	"0xeb628551b94ef928b8D32b5F94f9C9c1E8599652", # RandoMice
	"0xcBdcb6Ff9F6A80173EFb63Af006a36446946A95a", # The Habibiz
	"0xEC66944391b743D87A3146905C2B9b8b85B2bDf1", # tiny dinos
	"0x06D1a42382B2196eedDe76e0C90C3A49eE97233B", # Mutant Cats
	"0x145B65171c064738F65c99bfC59042a957aC5182", # wulf boy social club
	"0x5bd95E49994B4D637a3511B50c17ac115Dc31Fe8", # Metheors
	"0x2159762693C629C5A44Fc9baFD484f8B96713467", # MoonPets
	"0x16688d4047021755b7358f515864f706b1d24405", # Lost Souls
	"0x02A6DeC99B2Ca768D638fcD87A96F6069F91287c", # Moonfit
	"0x8fBE243D898e7c88A6724bB9eB13d746614D23d6", # GLMR Apes
	"0x139e9BA28D64da245ddB4cF9943aA34f6d5aBFc5", # Canary Network Agency
	"0x648763838b02054A237bdF86Cc1B70238cb50aF5", # Party Bears
	"0x756A9DC8181ABea18c2CC6575DCFcdD2c604aB6F", # Lyke Island Inhabitants
	"0x4316f538ed997e2e92ab92ee5c1b9f126e21578e", # Cosmos Kidz
	"0x332d68561a7aee5879a369411e059856d4580094", # Feline Fiendz
	"0xBc6219FC9f3521A8A566359906D6D0689c53DAcC", # Moonwalkers
	"0xbe1f1f4e1a4907d3a6debc110e1e9f551909c89c"] # ZOO DAO GEN 0


	royalty = ["0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Alley Katz
	"0xE8CC7A9e523886eF71783C6b3a8B49B421f8254d", # ALPACADABRAZ
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Dead Freaks
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Devious Demon Dudes
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Dumspter Dorks S1
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Dumpster Dorks S2
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # ELVEN
	"0xa5D55281917936818665c6cB87959b6a147D9306", # Ethlizards
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Fancy Birds
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # FLUF World
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Fluffy Polar Bears
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Holy Cows
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Humans Of The Metaverse
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Lobby Lobsters
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Luchadores
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Meta Eagle Club
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # MetaTravelers
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Monster Shelter
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # MoonCats
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # PixaWizards
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Polymorphs
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Purr Evil
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # RandoMice
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # The Habibiz
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # tiny dinos
	"0xb25a1D02B029d53212e4c356B6DaaD419762E606", # Mutant Cats
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # wulf boy social club
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Metheors
	"0x81145837A192B088c7fCA738a7E9Debab4F568F8", # MoonPets
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Lost Souls
	"0xC280b576e92212b0450558094969f7Cc928892e4", # Moonfit
	"0xd8C81D0706a027B870c20cC386BBffb15A36815e", # GLMR Apes
	"0xa25b6FefE3e397E179DB42837a5e424120243E6A", # Canary Network Agency
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Party Bears
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Lyke Island Inhabitants
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Cosmos Kidz
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Feline Fiendz
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b", # Moonwalkers
	"0x24410c1d93d1216E126b6A6cd32d79f634308b3b"] # ZOO DAO GEN 0

	### Currently, total of 39 collections and royalte recipient.

	ve_zoo.batchAllowNewContract(collections, royalty, {"from": account})
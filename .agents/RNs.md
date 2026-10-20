# Regras de negócios do SIGRAH

## RN01
- O cadastro de um cidadão pede menos informações e é aprovado automaticamente, enquanto para um administrador, é necessário mais informações e necessita de aprovação de outro administrador.
- RFs relacionadas: RF02, RF01

## RN02
- Somente o administrador tem permissão para cadastrar cano.
- RFs relacionadas: RF05

## RN03
- Os alertas são exibidos de forma anônima para todos os tipos de usuário.
- RFs relacionadas: RF09

## RN04
- Os alertas devem ser agrupados por local, quantidade e tipo para determinar o grau de urgência.
- RFs relacionadas: RF09

## RN05
- O mapa deve ser exibido na localização atual do usuário, caso tenha permissão, se não, deve exibir a localização padrão: Pau dos Ferros/RN.
- RFs relacionadas: RF03

## RN06
- Somente os alertas não resolvidos devem ser exibidos no mapa, ao serem resolvidos, são removidos da exibição.
- RFs relacionadas: RF09

## RN07
- Somente o cidadão pode criar alertas, o administrador não tem permissão para fazer isso.
- RFs relacionadas: RF08

## RN08
- Somente o administrador pode resolver o alerta, o cidadão não tem permissão para fazer isso.
- RFs relacionadas: RF10


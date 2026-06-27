def match_vulnerability(service, version, vulnerability_db):

    if service in vulnerability_db:

        if version in vulnerability_db[service]:

            return vulnerability_db[service][version]

    return None
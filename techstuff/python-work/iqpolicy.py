import nxiq
import pprint

host = 'http://localhost:8070'
user = 'admin'
passwd = 'admin123'

def main():

    c = nxiq.Connection(host, user, passwd) 
    
    orgs = c.getOrganizations()
    # nxiq.print (orgs)

    apps = c.getApplications()
    # nxiq.print(apps)

    i = c.getPolicyId('Security-High')
    # print (i)

    v = c.getPolicyViolations(i)
    # nxiq.print(v)
    
    o = c.getOrganizationId('smproto-org')
    # print (o)

    a = c.getApplicationId('jdom')
    print (a)

    g = c.getApplicationEvaluations('f13437f401674ee0bafbee1daca1ef7a')
    nxiq.print (g)

    

if __name__ == "__main__":
	main()


from flask import Blueprint, request
from service.AddressService import *
from service.AddressParse import *
from models.AlMaster import *
import json
from datetime import datetime

class Address:
    address_app = Blueprint('address_app', __name__, template_folder='templates')
    def __init__(self):
        pass

    @address_app.route('/address', methods=['GET'])
    def AddressByCompanyIdAndHubId():
        company_id = request.args.get('company_id')
        hub_id = request.args.get('hub_id')
        user_id = request.args.get('user_id')
        return getAddressByCompanyIdAndHubId(company_id, hub_id, user_id)

    @address_app.route('/parse', methods=['POST'])
    def parseAddressNormal():
        start = datetime.now()
        data = request.json
        result = normalParse(data)

        end = datetime.now()

        # print(end-start)

        return result

    @address_app.route('/getalmaster', methods=['POST'])
    def getalmaster():
        data = request.json
        possibleLevel = ['pincode','al3','al2', 'al1']
        if data is not None and data["levelName"] in possibleLevel:
            return getRelations(data["levelName"],data["value"],None,1,'th')
        return "Bad Request"
        # return normalParse(data)

    @address_app.route('/morelikethis', methods=['POST'])
    def morelikethis():
        data = request.json
        possibleLevel = ['sort_code','keyword']
        if data is not None and data["levelName"] in possibleLevel:
            return similarValues(data)
        return []

    @address_app.route('/addSyn', methods=['POST'])
    def addSyn():
        data = request.json
        addresses = data['addresses']
        company_id = data['companyId']
        user_id = data['userId']
        return addSyn(addresses, company_id, user_id)


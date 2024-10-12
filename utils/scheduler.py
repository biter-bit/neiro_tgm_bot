from db_api import api_profile_async, api_invoice_async, api_tariff_async
from services import logger, robokassa_obj
from utils.enum import PaymentName

async def update_limits():
    logger.info("Start update limits")
    try:
        await api_profile_async.update_limits_profile()
    except Exception as error:
        logger.error(f"ERROR update limits: {error}")
    finally:
        logger.info("Finish update limits")

async def check_subscription():
    logger.info("Start check subscription")
    profiles = await api_profile_async.get_profiles_finish_sub()
    for profile in profiles:
        try:
            if not profile.recurring:
                await api_profile_async.unsubscribe(profile.id)
                continue

            invoice_mother = await api_invoice_async.get_invoice_mother(profile.id)

            if not invoice_mother:
                await api_profile_async.unsubscribe(profile.id)
                continue

            invoice = await api_invoice_async.create_invoice(
                profile_id=profile.id, tariff_id=2, provider=PaymentName.ROBOKASSA
            )
            tariff = await api_tariff_async.get_tariff(invoice.tariff_id)

            robokassa_obj.recurring_request(
                user_id=profile.tgid,
                inv_id=invoice.id,
                price=tariff.price_rub,
                tariff_desc=tariff.description,
                mother_inv_id=invoice_mother.id,
            )
        except Exception as error:
            logger.error(f"ERROR with recurring payment | {profile} | {error} | {error.args}")
            continue

    logger.info("Finish check subscription")
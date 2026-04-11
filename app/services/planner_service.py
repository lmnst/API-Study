from app.prompt import Text_Test_Cases, Text_generate_plan
from app.schemas import PlanResponse, RequirementRequest, TestCases
from app.services.llm_service import call_openai_with_prompt
from app.utils import parse_llm_json, validate_requirement


async def generate_plan(request: RequirementRequest):

    # empty request validate 
    validate_requirement(request)

    # call LLM then return Response
    response = call_openai_with_prompt(Text_generate_plan, request)
    
    result = parse_llm_json(response, PlanResponse)
    return result


async def generate_test_cases(request: RequirementRequest):
    
    # empty request validate 
    validate_requirement(request)
    
    # call LLM then return Response
    response = call_openai_with_prompt(Text_Test_Cases, request)

    result = parse_llm_json(response, TestCases)
    return result

async def generate_workflow(request: RequirementRequest):
    result1 = await generate_plan(request)
    
    new_requirement = f"""
Original requirement:
{request.requirement}

Generated plan:
{result1.model_dump_json(indent=2)}

Please generate test cases based on the original requirement and the generated plan above.
"""
    
    request_new = RequirementRequest(requirement = new_requirement)
    
    result2 = await generate_test_cases(request_new)

    return {
        "plan": result1,
        "test_cases": result2
    }
